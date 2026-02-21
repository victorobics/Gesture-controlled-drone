# AI Gesture-Controlled CineWhoop (3-inch)

This project implements a compact, autonomous drone that replaces traditional RC controllers with real-time hand gesture recognition and human-following capabilities using **MediaPipe** and a **Raspberry Pi Zero 2 W**.

##  Technical Stack
*   **Vision System:** Raspberry Pi Zero 2 W + Camera Module 3 Wide (120° FOV).
*   **AI Framework:** Python 3.9 + MediaPipe (Optimized Lite) for 21-point hand landmark tracking.
*   **Positioning:** Optical Flow + Lidar Sensor (Matek 3901-L0X) for precise indoor hovering (Position Hold) without GPS.
*   **Flight Controller:** DarwinFPV F411 15A/25A AIO (running **iNav** for autonomous navigation).
*   **Communication:** MAVLink protocol via UART (GPIO 14/15) for real-time command injection.
*   **Chassis:** Cloud-149 V2 ducted frame for maximum indoor safety and human proximity.

##  Materials and Budget (BOM)


| Item | Model | Price (USD) | Price (EUR approx.) |
| :--- | :--- | :--- | :--- |
| **SBC (AI Brain)** | Raspberry Pi Zero 2 W | $25.00 | 23,50 € |
| **Camera (Eyes)** | RPi Camera Module 3 (Wide) | $40.00 | 38,00 € |
| **Positioning** | Matek Optical Flow & Lidar 3901-L0X | $39.00 | 37,00 € |
| **FC/ESC AIO** | DarwinFPV F411 15A ELRS AIO | $55.00 | 52,00 € |
| **Motors** | 4x 1404 4500KV Brushless | $50.00 | 47,00 € |
| **Frame** | Cloud-149 V2 (3" Ducted) | $35.00 | 33,00 € |
| **Power** | 2x 3S 850mAh LiPo (XT30) | $40.00 | 38,00 € |
| **Charger** | ISDT 608AC Smart Charger | $55.00 | 52,00 € |
| **Power Mgmt** | External BEC 5V/3A + Capacitor | $12.00 | 11,00 € |
| **Propellers** | Gemfan D76 5-Blade (3 Sets) | $16.00 | 15,00 € |
| **Storage & HW** | 32GB MicroSD + Cables/Bolts | $18.00 | 17,00 € |
| **TOTAL** | | **$385.00** | **~364,00 €** |

*Note: The remaining budget (~36€) is reserved for shipping costs, soldering materials, and emergency spares.*

##  System Connections (Diagram)

```text
      [ Camera Module 3 Wide ]

                |
          (CSI Ribbon Cable)
                |
      [ Raspberry Pi Zero 2 W ] <--- (Python / MediaPipe)

                |
        (GPIO 14 TX / 15 RX) -------- [ External BEC 5V/3A ]
                |                             |
        (MAVLink Data Link)            [ LiPo Battery 3S ]

                |                             |
      [ DarwinFPV F411 AIO ] <--- [ Optical Flow Sensor ]

        |          |          |          |
     [Mot 1]    [Mot 2]    [Mot 3]    [Mot 4]
