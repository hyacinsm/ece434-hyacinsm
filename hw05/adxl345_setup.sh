cd ~
./config-pin P9_21 i2c
./config-pin P9_22 i2c

cd /sys/class/i2c-adapter/i2c-2/
su 

echo adxl345 0x53 > new_device

echo "setup completed, but check console for error messages..."