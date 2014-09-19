#common for all custom begin
SHUT_ANIM = twd/custom/$(TWD_PROJECT)/$(TWD_CUST_NAME)/prebuilt/pwranim/shutanimation.zip
ifeq ($(SHUT_ANIM), $(wildcard $(SHUT_ANIM)))
TWD_PRODUCT_PROPERTY_OVERRIDES += \
    ro.operator.optr=CUST
endif
#common for all custom end 
