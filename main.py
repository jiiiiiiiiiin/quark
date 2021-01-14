import imu
import mpu6050
import ano_dt
import time



if __name__ == "__main__":
    mpu = mpu6050.mpu6050(0x68)
    mpu.set_gyro_range(0x18) # 设置陀螺仪范围 2000deg/s
    imu = imu.Mahony() # 姿态解算
    ANO_DT = ano_dt.ANO_DT() # 匿名上位机
    time_last = time.time()
    while(True):
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()
        f = 1 / (time.time() - time_last)
        time_last = time.time()
        angle = imu.MahonyAHRSupdateIMU(gyro_data['x'], gyro_data['y'], gyro_data['z'], accel_data['x'], accel_data['y'], accel_data['z'], f)
        ANO_DT.send_sensor(-angle[0], angle[1], angle[2])


