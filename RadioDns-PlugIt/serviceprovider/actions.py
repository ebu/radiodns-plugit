# -*- coding: utf-8 -*-

import imghdr
import os
import sys
import uuid

from flask import abort
from plugit.api import PlugItAPI
# Utils
from plugit.utils import action, only_orga_member_user, only_orga_admin_user, PlugItRedirect, json_only
from werkzeug.utils import secure_filename

import config
from actions_utils import get_orga_service_provider
from aws import awsutils
from models import db, ServiceProvider, LogoImage
from utils import send_image_to_mock_api


@action(route="/serviceprovider/", template="serviceprovider/home.html")
@only_orga_member_user()
def serviceprovider_home(request):
    """Show the serviceprovider."""

    orga, sp = get_orga_service_provider(request)

    saved = request.args.get('saved') == 'yes'
    deleted = request.args.get('deleted') == 'yes'

    # Default Image
    image_url_prefix = None
    default_logo = None

    return {'serviceprovider': sp.json if sp else None, 'ebu_codops': orga.codops, 'saved': saved, 'deleted': deleted}


@action(route="/serviceprovider/check")
@json_only()
@only_orga_member_user()
def serviceprovider_check(request):
    """Check AWS State for Service Provider."""

    plugitapi = PlugItAPI(config.API_URL)
    orga = plugitapi.get_orga(request.args.get('ebuio_orgapk'))

    sp = None
    if orga.codops:
        sp = ServiceProvider.query.filter_by(codops=orga.codops).order_by(ServiceProvider.codops).first()

    if sp and not config.STANDALONE:
        return sp.check_aws()

    return {'isvalid': False}


@action(route="/serviceprovider/edit/<id>", template="serviceprovider/edit.html", methods=['POST', 'GET'])
@only_orga_admin_user()
def serviceprovider_edit(request, id):
    """Edit a serviceprovider."""

    service_provider = None
    errors = []

    plugitapi = PlugItAPI(config.API_URL)
    orga = plugitapi.get_orga(request.args.get('ebuio_orgapk') or request.form.get('ebuio_orgapk'))

    if id != '-':
        service_provider = ServiceProvider.query.filter_by(id=id, codops=orga.codops).first()

    if not service_provider and id != '-':
        abort(404)

    if request.method == 'POST':

        if not service_provider:
            service_provider = ServiceProvider(int(request.form.get('ebuio_orgapk')))

        service_provider.codops = orga.codops
        service_provider.short_name = request.form.get('short_name')
        service_provider.medium_name = request.form.get('medium_name')
        service_provider.long_name = request.form.get('long_name')
        service_provider.short_description = request.form.get('short_description')
        service_provider.long_description = request.form.get('long_description')
        service_provider.url_default = request.form.get('url_default')
        service_provider.default_language = request.form.get('default_language')
        service_provider.location_country = request.form.get('location_country')

        service_provider.postal_name = request.form.get('postal_name')
        service_provider.street = request.form.get('street')
        service_provider.city = request.form.get('city')
        service_provider.zipcode = request.form.get('zipcode')
        service_provider.phone_number = request.form.get('phone_number')
        service_provider.keywords = request.form.get('keywords')

        # Check errors
        if service_provider.medium_name == '':
            errors.append("Please set a medium name")
        if service_provider.short_description == '':
            errors.append("Please set a short description")

        # If no errors, save
        if not errors:

            if not service_provider.id:
                db.session.add(service_provider)

            db.session.commit()

            return PlugItRedirect('serviceprovider/?saved=yes')

    if service_provider:
        service_provider = service_provider.json

    return {'object': service_provider, 'errors': errors}


@action(route="/serviceprovider/delete/<id>")
@json_only()
@only_orga_admin_user()
def serviceprovider_delete(request, id):
    """Delete a ServiceProvider."""

    object = ServiceProvider.query.filter_by(orga=int(request.args.get('ebuio_orgapk')), id=int(id)).first()
    db.session.delete(object)
    db.session.commit()

    return PlugItRedirect('serviceprovider/?deleted=yes')


@action(route="/serviceprovider/images/", template="serviceprovider/images/home.html")
@only_orga_member_user()
def serviceprovider_gallery_home(request):
    """Show the list of images for a service provider."""

    list = []

    orga, sp = get_orga_service_provider(request)
    image_url_prefix = ""

    if sp:
        for elem in LogoImage.query.filter_by(service_provider_id=int(sp.id)).order_by(LogoImage.filename).all():
            list.append(elem.json)

        image_url_prefix = awsutils.get_public_urlprefix(sp)

    saved = request.args.get('saved') == 'yes'
    deleted = request.args.get('deleted') == 'yes'

    return {'list': list, 'image_url_prefix': image_url_prefix, 'saved': saved, 'deleted': deleted,
            'serviceprovider': sp.json if sp else None}


@action(route="/serviceprovider/images/edit/<id>", template="serviceprovider/images/edit.html", methods=['POST', 'GET'])
@only_orga_admin_user()
def serviceprovider_gallery_edit(request, id):
    """Edit an Image."""

    object = None
    errors = []

    plugitapi = PlugItAPI(config.API_URL)
    orga = plugitapi.get_orga(request.args.get('ebuio_orgapk') or request.form.get('ebuio_orgapk'))

    sp = None
    if orga.codops:
        sp = ServiceProvider.query.filter_by(codops=orga.codops).order_by(ServiceProvider.codops).first()

    if id != '-':
        object = LogoImage.query.filter_by(id=int(id)).first()

    if request.method == 'POST':

        if not object:
            object = LogoImage(int(request.form.get('ebuio_orgapk')))

        object.name = request.form.get('name')
        if sp:
            object.service_provider = sp
        object.codops = orga.codops

        def add_unique_postfix(fn):
            """__source__ = 'http://code.activestate.com/recipes/577200-make-unique-file-name/'"""
            if not os.path.exists(fn):
                return fn

            path, name = os.path.split(fn)
            name, ext = os.path.splitext(name)

            make_fn = lambda i: os.path.join(path, '%s(%d)%s' % (name, i, ext))

            for i in xrange(2, sys.maxint):
                uni_fn = make_fn(i)
                if not os.path.exists(uni_fn):
                    return uni_fn

            return None

        def unique_filename(fn):

            path, name = os.path.split(fn)
            name, ext = os.path.splitext(name)

            make_fn = lambda i: os.path.join(path, '%s%s' % (str(uuid.uuid4()), ext))

            for i in xrange(2, sys.maxint):
                uni_fn = make_fn(i)
                if not os.path.exists(uni_fn):
                    return uni_fn

            return None

        new_file = False
        if request.files:
            new_file = True

            file = request.files['file']

            imageDirectoryPath = './media/uploads/serviceprovider/images/'
            if not os.path.exists(imageDirectoryPath):
                os.makedirs(imageDirectoryPath)

            if file:
                filename = secure_filename(file.filename)
                full_path = os.path.join('./media/uploads/serviceprovider/images/', filename)
                if not config.DEBUG:
                    full_path = unique_filename(full_path)
                path, name = os.path.split(full_path)

                # Delete existing one and only create a unique filename otherwise
                if object.filename:
                    try:
                        os.unlink(object.filename)
                    except:
                        pass
                    name = object.filename
                    full_path = os.path.join(path, name)
                else:
                    object.filename = name

                saved = file.save(full_path)

            # Check errors
            if object.name == '':
                errors.append("Please set a name")

            if object.filename == '' or object.filename is None:
                errors.append("Please upload an image")
            else:

                if imghdr.what(full_path) not in ['jpeg', 'png']:
                    errors.append("Image is not an png or jpeg image (it has header {})".format(imghdr.what(full_path)))
                    os.unlink(full_path)
                    object.filename = None
        else:
            errors.append("You must choose an image.")
            return {'errors': errors}

        # Check that we actually wrote the file
        if not os.path.isfile(full_path):
            errors.append(
                    "Something went wrong while transforming your image. Try again later or contact the administration.")

        # If no errors, save
        if not errors:

            # Upload MAIN Image to s3
            if new_file:

                # Based on what size to replace only upload the required ones
                replace_size = request.form.get('replace_size')

                if not replace_size:
                    try:
                        if config.STANDALONE:
                            send_image_to_mock_api({name: open(full_path, 'rb')})
                        else:
                            awsutils.upload_public_image(sp, name, full_path)
                    except:
                        pass

                # Create Required Image Sizes
                from PIL import Image
                for size in config.RADIODNS_REQUIRED_IMAGESIZES:
                    size_prefix = '%dx%d' % (size[0], size[1])
                    if not replace_size or replace_size == size_prefix:
                        image = Image.open(full_path)
                        if image.size != (size[0], size[1]):
                            image.thumbnail(size, Image.ANTIALIAS)
                            background = Image.new('RGBA' if image.mode in ('RGBA', 'LA') else 'RGB', size, (255, 255, 255, 0))
                            background.paste(image, ((size[0] - image.size[0]) / 2, (size[1] - image.size[1]) / 2))
                            if config.DEBUG:
                                pos = full_path.rfind(".")
                                unique_path = full_path[:pos] + size_prefix + full_path[pos:]
                            else:
                                unique_path = unique_filename(full_path)
                            background.save(unique_path)
                        else:
                            # Keep original since size Match !
                            unique_path = full_path
                        # Upload to s3
                        try:
                            s3filename = size_prefix + '/' + name
                            if config.STANDALONE:
                                send_image_to_mock_api({name: open(unique_path, 'rb')}, size_prefix)
                            else:
                                awsutils.upload_public_image(sp, s3filename, unique_path)

                            if size == (32, 32):
                                object.url32x32 = s3filename
                            if size == (112, 32):
                                object.url112x32 = s3filename
                            if size == (128, 128):
                                object.url128x128 = s3filename
                            if size == (320, 240):
                                object.url320x240 = s3filename
                            if size == (600, 600):
                                object.url600x600 = s3filename
                        except:
                            pass

                        # Delete Temporary file
                        os.unlink(unique_path)

            if not object.id:
                db.session.add(object)
            else:
                import glob
                for f in glob.glob('media/uploads/serviceprovider/cache/*_L%s.png' % (object.id,)):
                    os.unlink(f)

            db.session.commit()

            try:
                # Remove local copy
                os.unlink(full_path)
            except:
                pass

            return PlugItRedirect('serviceprovider/images/?saved=yes')

        try:
            # Remove local copy
            os.unlink(full_path)
        except:
            pass

    if object:
        object = object.json

    return {'object': object, 'sizes': config.RADIODNS_REQUIRED_IMAGESIZES, 'errors': errors}


@action(route="/serviceprovider/images/default/<id>")
@json_only()
@only_orga_admin_user()
def serviceprovider_gallery_setdefault(request, id):
    """Delete an Image."""

    plugitapi = PlugItAPI(config.API_URL)
    orga = plugitapi.get_orga(request.args.get('ebuio_orgapk') or request.form.get('ebuio_orgapk'))

    sp = None
    if orga.codops:
        sp = ServiceProvider.query.filter_by(codops=orga.codops).order_by(ServiceProvider.codops).first()

    if sp:
        object = LogoImage.query.filter_by(codops=orga.codops, id=int(id)).first()

        if object:
            sp.default_logo_image = object

            db.session.commit()

    return PlugItRedirect('serviceprovider/?saved=yes')


@action(route="/serviceprovider/images/delete/<id>")
@json_only()
@only_orga_admin_user()
def serviceprovider_gallery_delete(request, id):
    """Delete an Image."""

    plugitapi = PlugItAPI(config.API_URL)
    orga = plugitapi.get_orga(request.args.get('ebuio_orgapk') or request.form.get('ebuio_orgapk'))

    sp = None
    if orga.codops:
        sp = ServiceProvider.query.filter_by(codops=orga.codops).order_by(ServiceProvider.codops).first()

    object = LogoImage.query.filter_by(codops=orga.codops, id=int(id)).first()

    # Remove File
    try:
        os.unlink(object.filename)
    except:
        pass
    # Remove from S3
    try:
        awsutils.delete_public_image(sp, object.filename)
    except:
        pass

    # Remove from S3 other sizes
    for size in config.RADIODNS_REQUIRED_IMAGESIZES:
        filename_prefix = '%dx%d/' % (size[0], size[1])
        try:
            awsutils.delete_public_image(sp, filename_prefix + object.filename)
        except:
            pass

    import glob
    for f in glob.glob('media/uploads/serviceprovider/cache/*_L%s.png' % (object.id,)):
        os.unlink(f)

    db.session.delete(object)
    db.session.commit()

    return PlugItRedirect('serviceprovider/images/?deleted=yes')
