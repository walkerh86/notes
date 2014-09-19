#+ by hcj for customize

LOCAL_PATH:= $(call my-dir)

src = $(wildcard $(LOCAL_PATH)/*.zip $(LOCAL_PATH)/*.mp3)
PRODUCT_COPY_FILES += \
	$(foreach s,$(src),$(s):system/media/$(notdir $(s)))
