#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

import dlib
import face_recognition_models as frm
import numpy as np

from .face_det.face_det_mtcnn import FaceDetectorMTCNN

_pose_predictor = dlib.shape_predictor(
    frm.pose_predictor_model_location()
)

_face_encoder = dlib.face_recognition_model_v1(
    frm.face_recognition_model_location()
)


class FaceRecCoreV1:
    DfFaceRecConfid = 0.71

    @classmethod
    def gen_face_desc(
            cls,
            np_image,
            face_rect=None,
            num_jitters=1,
            detector=FaceDetectorMTCNN
    ):
        """
        Given an image, return the 128-dimension face encoding face in the image.

        :param np_image: The image that contains one or more faces
        :param face_rect: Optional - the bounding box of face if you already know them.
        :param num_jitters: How many times to re-sample the face when calculating encoding.
            Higher is more accurate, but slower (i.e. 100 is 100x slower)
        :param detector:
        :return: A list of 128-dimensional face encoding
        """
        raw_landmark = cls.gen_face_landmark(np_image, face_rect=face_rect, detector=detector)

        if raw_landmark is None:
            return None

        return np.array(
            _face_encoder.compute_face_descriptor(
                np_image,
                raw_landmark,
                num_jitters,
            )
        )

    @classmethod
    def gen_face_landmark(
            cls,
            np_image,
            face_rect=None,
            detector=FaceDetectorMTCNN
    ):
        if face_rect is None:
            face_rects = detector.sdetect(
                np_image,
                FaceDetectorMTCNN.Confid,
                output_type=1
            )
            face_rect = largest_dlib_rect(face_rects)

        if face_rect is None:
            return None

        return _pose_predictor(np_image, face_rect)

    @classmethod
    def gen_face_landmarks(
            cls,
            np_image,
            face_rects=None,
            detector=FaceDetectorMTCNN
    ):
        if face_rects is None:
            face_rects = detector.sdetect(
                np_image,
                FaceDetectorMTCNN.Confid,
                output_type=1
            )

        return [
            _pose_predictor(np_image, face_location) for face_location in face_rects
        ]

    @classmethod
    def gen_face_desc_from_landmark(
            cls,
            np_image,
            landmark,
            num_jitters=1
    ):
        return np.array(
            _face_encoder.compute_face_descriptor(
                np_image,
                landmark,
                num_jitters,
            )
        )

    @classmethod
    def gen_face_descs_from_landmarks(
            cls,
            np_image,
            landmarks,
            num_jitters=1
    ):
        return [
            np.array(
                _face_encoder.compute_face_descriptor(
                    np_image,
                    raw_landmark_set,
                    num_jitters,
                )
            ) for raw_landmark_set in landmarks
        ]


def largest_dlib_rect(rects):
    if rects is None or len(rects) == 0:
        return None
    largest_rect = rects[0]
    largest_area = largest_rect.area()

    for face in rects[1:]:
        face_area = face.area()
        if face_area > largest_area:
            largest_rect, largest_area = face, face_area

    return largest_rect
