#+ by hcj for customize

LOCAL_PATH:= $(call my-dir)

RINGTONE_PATH = $(LOCAL_PATH)/ringtones
src = $(wildcard $(RINGTONE_PATH)/*.*)
PRODUCT_COPY_FILES += \
	$(foreach s,$(src),$(s):system/media/audio/ringtones/$(notdir $(s)))
	
ALARM_PATH = $(LOCAL_PATH)/alarms
src = $(wildcard $(ALARM_PATH)/*.*)
PRODUCT_COPY_FILES += \
	$(foreach s,$(src),$(s):system/media/audio/alarms/$(notdir $(s)))
	
NOTIFICATION_PATH = $(LOCAL_PATH)/notifications
src = $(wildcard $(NOTIFICATION_PATH)/*.*)
PRODUCT_COPY_FILES += \
	$(foreach s,$(src),$(s):system/media/audio/notifications/$(notdir $(s)))