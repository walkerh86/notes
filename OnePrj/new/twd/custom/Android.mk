#by hcj for customize

LOCAL_PATH := $(call my-dir)
#var LOCAL_PATH wound be changed after call first-makefiles-under,
#so copy LOCAL_PATH
LOCAL_PATH_BAK := $(findstring $(LOCAL_PATH),$(LOCAL_PATH))

ifneq ($(TWD_PROJECT),)
   ifneq ($(TWD_CUST_NAME),)
       TWD_COMMON_DIR = $(LOCAL_PATH_BAK)/common
       include $(call first-makefiles-under,$(TWD_COMMON_DIR))

       TWD_PRJ_DIR = $(LOCAL_PATH_BAK)/$(TWD_PROJECT)

       TWD_PRJ_COMMON_DIR = $(TWD_PRJ_DIR)/common
       include $(call first-makefiles-under,$(TWD_PRJ_COMMON_DIR))

       TWD_PRJ_CUST_DIR := $(TWD_PRJ_DIR)/$(TWD_CUST_NAME)
       filter_dirs = $(TWD_PRJ_CUST_DIR)/prebuilt $(TWD_PRJ_CUST_DIR)/preinstall
       all_cust_mk_files := 
       $(foreach sub_dir,$(filter_dirs), $(eval $(info sub_dir $(sub_dir)) all_cust_mk_files += $(call first-makefiles-under,$(sub_dir))))
#       $(info all_cust_mk_files $(all_cust_mk_files))
       include $(all_cust_mk_files)
   endif
endif
