import json


class DefaultConfig:
  process_config = {
    "confidence_filter": 0.71,
    "show_monitor": "true",
    "video_config": {
      "scale_width": 960,
      "scale_height": -1
    },
    "face_detection_config": {
      "detector": "tf",
      "confidence_filter": 0.2
    },
    "middle_filters": [
      {
        "filter_name": "MfZone",
        "filter_config": {
          "zone_points": [
            [
              200,
              60
            ],
            [
              760,
              60
            ],
            [
              760,
              540
            ],
            [
              200,
              540
            ],
            [
              200,
              60
            ]
          ],
          "filter_mode": 0
        }
      },
      {
        "filter_name": "MfRectSize",
        "filter_config": {
          "min_size": 4000,
          "max_size": -1,
          "filter_mode": 0
        }
      }
    ],
    "anti_phone_filter": {
      "filter_name": "MfAntiPhone",
      "filter_config": {
        "phone_detector": "p",
        "phone_detection_config": {
          "min_area": 5000,
          "min_diagona": 100,
          "min_asp": 0.3,
          "max_asp": 3.0
        },
        "zone_points": [
          [
            180,
            0
          ],
          [
            900,
            0
          ],
          [
            900,
            550
          ],
          [
            180,
            550
          ],
          [
            180,
            0
          ]
        ],
        "filter_mode": 1
      },
      "notify_interval": 1000,
      "enabled": 'true'
    },
    "black_list_config": {
      "enabled": 'false',
      "alert_interval": 5000
    },
    "unknown_face_config": {
      "cache": 0,
      "reset_interval": 5000,
      "confidence_filter": 0.62
    }
  }
  data = json.loads(json.dumps(process_config))