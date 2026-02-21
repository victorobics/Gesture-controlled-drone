#  AI Gesture-Controlled CineWhoop (3-inch)

This project implements a compact, safe drone that replaces traditional RC controllers with real-time hand gesture recognition using MediaPipe and a Raspberry Pi Zero 2 W.

#  Technical Stack
*   **Vision System:** Raspberry Pi Zero 2 W + Camera Module 3 Wide (120° FOV).
*   **AI Framework:** Python 3.9 + MediaPipe for 21-point hand landmark tracking.
*   **Flight Controller:** DarwinFPV F411 15A AIO (Integrated FC + ESC).
*   **Communication:** MAVLink protocol via UART (GPIO 14/15) for real-time command injection.
*   **Chassis:** Cloud-149 V2 ducted frame for indoor safety.

#  Verified Parts List & Budget (BOM)


| Item | Model | Price (USD) | Precio (EUR aprox.) |
| :--- | :--- | :--- | :--- |
| **SBC (AI Brain)** | Raspberry Pi Zero 2 W | $20.00 | 19,50 € |
| **Camera (Eyes)** | RPi Camera Module 3 (Wide) | $35.00 | 33,00 € |
| **FC/ESC AIO** | DarwinFPV F411 15A AIO | $55.00 | 52,00 € |
| **Motors** | 4x 1404 4500KV Brushless | $55.00 | 52,00 € |
| **Frame** | Cloud-149 V2 (3" Ducted) | $35.00 | 33,00 € |
| **Battery** | 3S 850mAh LiPo (XT30) | $20.00 | 19,00 € |
| **Charger** | ISDT 608AC Smart Charger | $55.00 | 52,00 € |
| **SD & Props** | 32GB MicroSD + 2x Sets Props | $25.00 | 24,00 € |
| **TOTAL** | | **$300.00** | **~284,50 €** |

#  System Connections (Diagram)
```text
  [ Camera Module 3 Wide ]

            |
      (CSI Ribbon Cable)
            |
  [ Raspberry Pi Zero 2 W ] <--- (Python / MediaPipe)

            |
    (GPIO 14 TX / 15 RX)
            |
    (UART Data Link / MAVLink)

            |
  [ DarwinFPV F411 AIO ] <--- (iNav / Betaflight)
    |          |          |          |
 [Motor 1]  [Motor 2]  [Motor 3]  [Motor 4]
