import casperfpga,time

f=casperfpga.SkarabFpga('10.99.37.5')
#f.upload_to_ram_and_program('test_hmc_vacc1_2017-3-31_1403.fpg') #180MHz
f.upload_to_ram_and_program('test_hmc_vacc1_2017-3-29_1700.fpg') #156.25MHz
f.registers.vacctvg_control.write(sync_sel=1,valid_sel=1,data_sel=1)
f.registers.vacctvg_control.write(ctr_en=1)
f.registers.vacctvg_control.write(vector_en=1)
#f.registers.vacctvg_control.write(reset='pulse')

f.registers.vacc_rst=1
f.registers.hmc_vacc_ctrl_rb_disable=1

f.registers.acc_len.write(reg=200)


f.registers.vacc_tvg0_n_per_group.write(reg=12) # 180MHz
#f.registers.vacc_tvg0_n_per_group.write(reg=14) #156.25MHz
f.registers.vacc_tvg0_group_period.write(reg=20)
f.registers.vacc_tvg0_n_pulses.write(reg=2001000)


#prep the snap block:
f.snapshots.snap_acc.arm()
#f.snapshots.snap_acc.arm(man_trig=True)
f.snapshots.hmc_vacc_hmc_in_rd_snap_ss.arm()
f.snapshots.hmc_vacc_hmc_in_wr_snap_ss.arm()
f.snapshots.hmc_vacc_hmc_out_snap_ss.arm()
f.snapshots.hmc_vacc_qdr_out_snap_ss.arm()
f.snapshots.hmc_vacc_ctrl_snap_ss.arm()
f.registers.hmc_vacc_cnt_rst.write(reg='pulse')

print 'hmc status: ',f.registers.hmc_vacc_hmc_status.read()['data']
print 'err status: ',f.registers.hmc_vacc_err_status.read()['data']

f.registers.vacc_rst=0


#start the TVG running:
f.registers.vacctvg_control.write(reset=True,pulse_en=False)
f.registers.vacctvg_control.write(reset=False,pulse_en=True)
time.sleep(2)

print "hmc rd cnt:",f.registers.hmc_vacc_hmc_rd_cnt.read_uint()
print "hmc out cnt:",f.registers.hmc_vacc_hmc_out_cnt.read_uint()
print "reorder out cnt:",f.registers.hmc_vacc_reord_out_cnt.read_uint()
print "fifo wr cnt:",f.registers.hmc_vacc_fifo_wr_cnt.read_uint()
print "fifo rd cnt:",f.registers.hmc_vacc_fifo_rd_cnt.read_uint()
print "hmc wr cnt:",f.registers.hmc_vacc_hmc_wr_cnt.read_uint()
print "fifo out cnt:",f.registers.hmc_vacc_fifo_out_cnt.read_uint()
print "reorder miss cnt:",f.registers.hmc_vacc_reord_miss_cnt.read_uint()

qdr=f.snapshots.hmc_vacc_qdr_out_snap_ss.read(read_nowait=True)
li=0
for i,t in enumerate(qdr['data']['tag']):
    if qdr['data']['qdr_valid'][i]:
        if ((qdr['data']['tag'][li]-t) != -1) and ((qdr['data']['tag'][li]-t) != 511): 
            print i,t
        li=i
hmc=f.snapshots.hmc_vacc_hmc_out_snap_ss.read(read_nowait=True)
md=0
mi=0
for i,t in enumerate(hmc['data']['tag']):
    diff=hmc['data']['reord_max'][i]-t
    if diff<0:
        diff+=512
    if diff > md:
        md=diff
        mi=i
    #print i,t, diff, md
print "Max out of order: %i at idx %i"%(md,mi)
