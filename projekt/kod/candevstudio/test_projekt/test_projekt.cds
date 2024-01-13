{
    "connections": [
        {
            "in_id": "{284222a1-1869-4fee-b3d8-ad50dd7bfb74}",
            "in_index": 0,
            "out_id": "{e70e0e8d-7b04-42f3-8be4-d11df53da371}",
            "out_index": 0
        }
    ],
    "nodes": [
        {
            "id": "{e70e0e8d-7b04-42f3-8be4-d11df53da371}",
            "model": {
                "caption": "CanRawSender #21",
                "content": [
                    {
                        "data": "0000000000000001",
                        "id": "001",
                        "interval": "500",
                        "loop": true,
                        "remote": false,
                        "send": false
                    }
                ],
                "name": "CanRawSender",
                "senderColumns": [
                    "Id",
                    "Data",
                    "Remote",
                    "Loop",
                    "Interval",
                    ""
                ],
                "sorting": {
                    "currentIndex": 0
                }
            },
            "position": {
                "x": 368,
                "y": 221
            }
        },
        {
            "id": "{284222a1-1869-4fee-b3d8-ad50dd7bfb74}",
            "model": {
                "QML file": "/home/lgm/fer/diplomski/projekt/kod/candevstudio/test_projekt/simple_timer.qml",
                "caption": "QMLExecutor #14",
                "name": "QMLExecutor"
            },
            "position": {
                "x": 816,
                "y": 395
            }
        }
    ]
}
