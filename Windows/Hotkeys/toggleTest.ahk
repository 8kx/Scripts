; Define the hotkey (Ctrl + Alt + F)
^!f::
    deviceName := "OpenComm by Shokz"

    DllCall("LoadLibrary", "str", "Bthprops.cpl", "ptr")
    VarSetCapacity(BLUETOOTH_DEVICE_SEARCH_PARAMS, 24+A_PtrSize*2, 0)
    NumPut(24+A_PtrSize*2, BLUETOOTH_DEVICE_SEARCH_PARAMS, 0, "uint")
    NumPut(1, BLUETOOTH_DEVICE_SEARCH_PARAMS, 4, "uint")   ; fReturnAuthenticated
    VarSetCapacity(BLUETOOTH_DEVICE_INFO, 560, 0)
    NumPut(560, BLUETOOTH_DEVICE_INFO, 0, "uint")
    loop
    {
        if (A_Index = 1) {
            foundedDevice := DllCall("Bthprops.cpl\BluetoothFindFirstDevice", "ptr", &BLUETOOTH_DEVICE_SEARCH_PARAMS, "ptr", &BLUETOOTH_DEVICE_INFO, "ptr")
            if !foundedDevice {
                MsgBox, No Bluetooth devices found
                return
            }
        } else {
            if !DllCall("Bthprops.cpl\BluetoothFindNextDevice", "ptr", foundedDevice, "ptr", &BLUETOOTH_DEVICE_INFO) {
                MsgBox, Device not found
                break
            }
        }
        dev := StrGet(&BLUETOOTH_DEVICE_INFO + 64)
        if (dev = deviceName) {
            VarSetCapacity(Handsfree, 16)
            DllCall("ole32\CLSIDFromString", "wstr", "{0000111e-0000-1000-8000-00805f9b34fb}", "ptr", &Handsfree)
            VarSetCapacity(AudioSink, 16)
            DllCall("ole32\CLSIDFromString", "wstr", "{0000110b-0000-1000-8000-00805f9b34fb}", "ptr", &AudioSink)

            ; Disconnect services
            hr1 := DllCall("Bthprops.cpl\BluetoothSetServiceState", "ptr", 0, "ptr", &BLUETOOTH_DEVICE_INFO, "ptr", &Handsfree, "int", 0)
            hr2 := DllCall("Bthprops.cpl\BluetoothSetServiceState", "ptr", 0, "ptr", &BLUETOOTH_DEVICE_INFO, "ptr", &AudioSink, "int", 0)


            if (hr1 = 0) and (hr2 = 0)
                break
            else
            {            
                ; Reconnect services
                hr1 := DllCall("Bthprops.cpl\BluetoothSetServiceState", "ptr", 0, "ptr", &BLUETOOTH_DEVICE_INFO, "ptr", &Handsfree, "int", 1)
                hr2 := DllCall("Bthprops.cpl\BluetoothSetServiceState", "ptr", 0, "ptr", &BLUETOOTH_DEVICE_INFO, "ptr", &AudioSink, "int", 1)
            }
            ; if (hr1 = 0) and (hr2 = 0)
            ;     MsgBox, Successfully toggled services for %deviceName%
            ; else
            ;     MsgBox, Error toggling services for %deviceName%

            break
        }
    }

    DllCall("Bthprops.cpl\BluetoothFindDeviceClose", "ptr", foundedDevice)
    ExitApp
return