#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

from threading import Lock

import dlib

from .detect_face import *
import tensorflow as tf

DfFaceDetConfid = 0.4


class FaceDetectorMTCNN:
    Confid = DfFaceDetConfid

    _model_loaded = False
    _load_model_lock = Lock()

    pnet, rnet, onet = None, None, None
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    @classmethod
    def load_model(cls):
        if cls._model_loaded:
            return

        with cls._load_model_lock:
            if cls._model_loaded:
                return

            cls._tf_graph = tf.Graph()
            with cls._tf_graph.as_default():
                # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1)
                # sess = tf.Session(back_end=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
                config = tf.ConfigProto()
                config.gpu_options.allow_growth = True
                sess = tf.Session(graph=cls._tf_graph, config=config)
                with sess.as_default():
                    cls.pnet, cls.rnet, cls.onet = create_mtcnn(sess, None)

            cls._model_loaded = True

    @classmethod
    def face_det(
            cls,
            np_image,
            output_type=1,
    ):
        bounding_boxes, _ = detect_face(
            np_image,
            cls.minsize, cls.pnet, cls.rnet, cls.onet, cls.threshold, cls.factor
        )
        result = []
        nrof_faces = bounding_boxes.shape[0]
        if nrof_faces > 0:
            det = bounding_boxes[:, 0:4]
            if nrof_faces > 1:
                if output_type == 1:
                    for i in range(nrof_faces):
                        rect = np.squeeze(det[i])
                        result.append(dlib.rectangle(
                            int(rect[0]),
                            int(rect[1]),
                            int(rect[2]),
                            int(rect[3])
                        ))
                else:
                    for i in range(nrof_faces):
                        rect = np.squeeze(det[i])
                        result.append({
                            'rect': {
                                'left': int(rect[0]),
                                'top': int(rect[1]),
                                'right': int(rect[2]),
                                'bottom': int(rect[3])
                            }
                        })
            else:
                rect = np.squeeze(det)
                if output_type == 1:
                    result.append(dlib.rectangle(
                        int(rect[0]),
                        int(rect[1]),
                        int(rect[2]),
                        int(rect[3])
                    ))
                else:
                    result.append({
                        'rect': {
                            'left': int(rect[0]),
                            'top': int(rect[1]),
                            'right': int(rect[2]),
                            'bottom': int(rect[3])
                        }
                    })

        return result

    @classmethod
    def sdetect(cls, np_image, confidence_filter=Confid, output_type=1):
        cls.load_model()

        return cls.face_det(
            np_image,
            output_type=output_type
        )
