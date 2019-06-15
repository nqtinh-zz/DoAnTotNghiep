#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

import os
import time

import cv2
import shortuuid

from config.django_settings import STATIC_DIR, STATIC_URL
# from config.log_config import log


class StaticServing:
    _StaticRoot = STATIC_DIR
    _StaticUrl = STATIC_URL
    _ResDir = os.path.join(_StaticRoot, 'res')
    _TmpDir = os.path.join(_StaticRoot, 'tmp')

    @classmethod
    def save_res(cls, multipart_files, sub_folders, names=None, extension='jpg'):
        file_paths = []
        serve_urls = []
        err = None

        try:
            folder = os.path.join(
                cls._ResDir,
                *sub_folders,
            )
            os.makedirs(folder, exist_ok=True)

            if names is None:
                names = [
                    f'{int(round(time.time() * 1000))}_{shortuuid.uuid()}'
                    for _ in range(len(multipart_files))
                ]

            for multipart_file, name in zip(multipart_files, names):
                file_path, serve_url, exc = cls._save(
                    multipart_file,
                    folder,
                    name=name,
                    extension=extension,
                )
                if exc is not None:
                    raise exc
                file_paths.append(file_path)
                serve_urls.append(serve_url)

        except Exception as exc:
            err = IOError(f'Save resource file failed: {exc}')
            # log.error(f'{err}')

        finally:
            return file_paths, serve_urls, err

    @classmethod
    def save_tmp(cls, multipart_files, extension='jpg'):
        file_paths = []
        serve_urls = []
        err = None

        try:
            os.makedirs(cls._TmpDir, exist_ok=True)

            for multipart_file in multipart_files:
                file_path, serve_url, exc = cls._save(
                    multipart_file,
                    cls._TmpDir,
                    extension=extension,
                )
                if exc is not None:
                    raise exc
                file_paths.append(file_path)
                serve_urls.append(serve_url)

        except Exception as exc:
            err = IOError(f'Save tmp file failed: {exc}')
            # log.error(f'{err}')

        finally:
            return file_paths, serve_urls, err

    @classmethod
    def save_res_npimage(cls, np_images, sub_folders, names=None, extension='jpg'):
        file_paths = []
        serve_urls = []
        err = None

        try:
            folder = os.path.join(
                cls._ResDir,
                *sub_folders,
            )
            os.makedirs(folder, exist_ok=True)

            if names is None:
                names = [
                    f'{int(round(time.time() * 1000))}_{shortuuid.uuid()}'
                    for _ in range(len(np_images))
                ]

            for np_image, name in zip(np_images, names):
                file_path, serve_url, exc = cls._save_npimage(
                    np_image,
                    folder,
                    name=name,
                    extension=extension,
                )
                if exc is not None:
                    raise exc
                file_paths.append(file_path)
                serve_urls.append(serve_url)

        except Exception as exc:
            err = IOError(f'Save resource file failed: {exc}')
            # log.error(f'{err}')

        finally:
            return file_paths, serve_urls, err

    @classmethod
    def save_tmp_npimage(cls, np_images, extension='jpg'):
        file_paths = []
        serve_urls = []
        err = None

        try:
            os.makedirs(cls._TmpDir, exist_ok=True)

            for np_image in np_images:
                file_path, serve_url, exc = cls._save_npimage(
                    np_image,
                    cls._TmpDir,
                    extension=extension,
                )
                if exc is not None:
                    raise exc
                file_paths.append(file_path)
                serve_urls.append(serve_url)

        except Exception as exc:
            err = IOError(f'Save tmp file failed: {exc}')
            # log.error(f'{err}')

        finally:
            return file_paths, serve_urls, err

    @classmethod
    def delete(cls, serve_url=None, file_path=None):
        try:
            if file_path is None:
                if serve_url is None:
                    return None
                file_path = cls.serve_url_2_path(serve_url)

            err = cls._delete(file_path)

        except Exception as exc:
            err = IOError(f'Delete file failed: {exc}')
            # log.error(f'{err}')

        return err

    @classmethod
    def rename(cls, serve_url=None, file_path=None, new_file_name=None, new_extension=None):
        new_file_path = ''
        new_serve_url = ''
        err = None

        try:
            if file_path is None:
                if serve_url is None:
                    raise ValueError('Please specify serve_url or file_path of the file')
                file_path = cls.serve_url_2_path(serve_url)

            if new_extension is None:
                _, old_extension = os.path.splitext(file_path)
                new_extension = old_extension

            new_file_path = os.path.join(
                os.path.dirname(file_path),
                f'{new_file_name}{new_extension}',
            )

            err = cls._rename(file_path, new_file_path)
            if err is not None:
                raise err

            new_serve_url = cls.path_2_serve_url(new_file_path)

        except Exception as exc:
            err = IOError(f'Rename file failed: {exc}')
            # log.error(f'{err}')

        return new_file_path, new_serve_url, err

    @classmethod
    def _save(cls, multipart_file, folder, name=None, extension='jpg'):
        if name is None:
            name = f'{int(round(time.time() * 1000))}_{shortuuid.uuid()}'

        if extension[0] == '.':
            extension = extension[1:]

        file_path = os.path.join(folder, f'{name}.{extension}')
        serve_url = cls.path_2_serve_url(file_path)
        err = None

        try:
            with open(file_path, 'wb+') as dest:
                for chunk in multipart_file.chunks():
                    dest.write(chunk)

        except Exception as exc:
            err = exc
            # log.error(f'Save file failed: {exc}')

        finally:
            return file_path, serve_url, err

    @classmethod
    def _save_npimage(cls, np_image, folder, name=None, extension='jpg'):
        if name is None:
            name = f'{int(round(time.time() * 1000))}_{shortuuid.uuid()}'

        if extension[0] == '.':
            extension = extension[1:]

        file_path = os.path.join(folder, f'{name}.{extension}')
        serve_url = cls.path_2_serve_url(file_path)
        err = None

        try:
            cv2.imwrite(file_path, np_image)

        except Exception as exc:
            err = exc
            # log.error(f'Save file failed: {exc}')

        finally:
            return file_path, serve_url, err

    @classmethod
    def _delete(cls, file_path):
        err = None

        try:
            if os.path.exists(file_path):
                os.remove(
                    file_path
                )

        except Exception as exc:
            err = exc
            # log.error(f'Delete file failed: {exc}')

        return err

    @classmethod
    def _rename(cls, file_path, new_file_path):
        err = None

        try:
            os.renames(file_path, new_file_path)

        except Exception as exc:
            err = exc
            # log.error(
            #     f'Rename file [{file_path}] to [{new_file_path}] failed: '
            #     f'{exc}'
            # )

        finally:
            return err

    @classmethod
    def serve_url_2_path(cls, serve_url: str) -> str:
        file_path = os.path.join(
            cls._StaticRoot,
            serve_url[len(cls._StaticUrl):],
        )
        return file_path

    @classmethod
    def path_2_serve_url(cls, file_path: str) -> str:
        serve_url = os.path.relpath(file_path, cls._StaticRoot)
        serve_url = '{}{}'.format(cls._StaticUrl, serve_url.replace('\\', '/'))
        return serve_url
