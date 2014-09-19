#+ by hcj for customize

LOCAL_PATH:= $(call my-dir)

src_apk = $(wildcard $(LOCAL_PATH)/*.apk)
PRODUCT_COPY_FILES += \
	$(foreach s_apk,$(src_apk),$(s_apk):system/app/$(notdir $(s_apk)))
	
src_so = $(wildcard $(LOCAL_PATH)/*.so)
PRODUCT_COPY_FILES += \
	$(foreach s_so,$(src_so),$(s_so):system/lib/$(notdir $(s_so)))
