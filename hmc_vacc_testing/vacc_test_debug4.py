import casperfpga,time

f=casperfpga.SkarabFpga('10.99.55.170')
#f.upload_to_ram_and_program('test_hmc_vacc1_2017-3-31_1403.fpg') #180MHz
f.upload_to_ram_and_program('test_hmc_vacc_half_2017-5-17_1603.fpg')
f.registers.vacctvg_control.write(sync_sel=1,valid_sel=1,data_sel=1,ctr_en=1,vector_en=1,pulse_en=False)
#f.registers.vacctvg_control.write(reset='pulse')
f.registers.vacctvg_control.write(reset=1) #hold vacc in reset; allow memory to erase.
f.registers.vacctvg_control.write(cnt_rst='pulse') #reset all counters to zero


for vacc_n in range(4):
    print '\n\n'
    print 'HMC VACC %i'%vacc_n
    print '=========='
    print "hmc rd cnt:",f.registers['hmc_vacc%i_hmc_rd_cnt'%vacc_n].read_uint()
    print "hmc out cnt:",f.registers['hmc_vacc%i_hmc_out_cnt'%vacc_n].read_uint()
    print "reorder out cnt:",f.registers['hmc_vacc%i_reord_out_cnt'%vacc_n].read_uint()
    print "fifo wr cnt:",f.registers['hmc_vacc%i_fifo_wr_cnt'%vacc_n].read_uint()
    print "fifo rd cnt:",f.registers['hmc_vacc%i_fifo_rd_cnt'%vacc_n].read_uint()
    print "hmc wr cnt:",f.registers['hmc_vacc%i_hmc_wr_cnt'%vacc_n].read_uint()
    print "fifo out cnt:",f.registers['hmc_vacc%i_fifo_out_cnt'%vacc_n].read_uint()
    print "reorder miss cnt:",f.registers['hmc_vacc%i_reord_miss_cnt'%vacc_n].read_uint()
    print 'err status: ',f.registers['hmc_vacc%i_err_status'%vacc_n].read()['data']

print "\n\nInitialising all VACCs and TVGs...!\n"

time.sleep(10)

f.registers.vacc_tvg0_n_per_group.write(reg=6)
f.registers.vacc_tvg0_group_period.write(reg=20)
#f.registers.vacc_tvg1_n_per_group.write(reg=5)
#f.registers.vacc_tvg1_group_period.write(reg=20)
f.registers.vacc_tvg2_n_per_group.write(reg=6)
f.registers.vacc_tvg2_group_period.write(reg=20)
f.registers.vacc_tvg3_n_per_group.write(reg=6)
f.registers.vacc_tvg3_group_period.write(reg=20)

f.registers.acc_len.write(reg=10)
f.registers.acc_len1.write(reg=10)
f.registers.acc_len2.write(reg=10)
f.registers.acc_len3.write(reg=10)

f.registers.vacc_tvg0_n_pulses.write(reg=3.5e6*10*2+200e3) #generate 2 full accumulations, plus another single     vector.
f.registers.vacc_tvg1_n_pulses.write(reg=3.5e6*10*2+200e3) #generate 2 full accumulations, plus another single     vector.
f.registers.vacc_tvg2_n_pulses.write(reg=3.5e6*10*2+200e3) #generate 2 full accumulations, plus another single     vector.
f.registers.vacc_tvg3_n_pulses.write(reg=3.5e6*10*2+200e3) #generate 2 full accumulations, plus another single     vector.

time.sleep(1)
f.registers.vacctvg_control.write(cnt_rst='pulse')

f.snapshots.snap_acc.arm(man_trig=True)
f.snapshots.snap_acc1.arm(man_trig=True)
f.snapshots.snap_acc2.arm(man_trig=True)
f.snapshots.snap_acc3.arm(man_trig=True)

#f.snapshots.snap_acc.arm(man_trig=True)
f.snapshots.hmc_vacc0_hmc_in_rd_snap_ss.arm(circular_capture=True)
f.snapshots.hmc_vacc0_hmc_in_wr_snap_ss.arm(circular_capture=True)
f.snapshots.hmc_vacc0_hmc_out_snap_ss.arm(circular_capture=True)
f.snapshots.hmc_vacc0_qdr_out_snap_ss.arm(circular_capture=True)
f.snapshots.hmc_vacc0_ctrl_snap_ss.arm(circular_capture=True)

print 'fifo status: ',f.registers.hmc_vacc0_fifo_status.read()['data']
print 'err status: ',f.registers.hmc_vacc0_err_status.read()['data']

#start the TVG running:
print "\n\nBringing VACCs out of reset..."
f.registers.vacctvg_control.write(reset=False,pulse_en=False) #keep tvgs disabled.
time.sleep(0.1)
for vacc_n in range(4):
    print "hmc rd cnt:",f.registers['hmc_vacc%i_hmc_rd_cnt'%vacc_n].read_uint()
    print "hmc out cnt:",f.registers['hmc_vacc%i_hmc_out_cnt'%vacc_n].read_uint()
    print "reorder out cnt:",f.registers['hmc_vacc%i_reord_out_cnt'%vacc_n].read_uint()
    print "fifo wr cnt:",f.registers['hmc_vacc%i_fifo_wr_cnt'%vacc_n].read_uint()
    print "fifo rd cnt:",f.registers['hmc_vacc%i_fifo_rd_cnt'%vacc_n].read_uint()
    print "hmc wr cnt:",f.registers['hmc_vacc%i_hmc_wr_cnt'%vacc_n].read_uint()
    print "fifo out cnt:",f.registers['hmc_vacc%i_fifo_out_cnt'%vacc_n].read_uint()
    print "reorder miss cnt:",f.registers['hmc_vacc%i_reord_miss_cnt'%vacc_n].read_uint()
    print 'err status: ',f.registers['hmc_vacc%i_err_status'%vacc_n].read()['data']

print 'VACC0 fifo status: ',f.registers.hmc_vacc0_fifo_status.read()['data']
print "\n\nStarting accumulation...",
f.registers.vacctvg_control.write(reset=False,pulse_en=True)
time.sleep(2)
print "done."
for vacc_n in range(4):
    print '\n'
    print 'HMC VACC %i'%vacc_n
    print '=========='
    print "hmc rd cnt:",f.registers['hmc_vacc%i_hmc_rd_cnt'%vacc_n].read_uint()
    print "hmc out cnt:",f.registers['hmc_vacc%i_hmc_out_cnt'%vacc_n].read_uint()
    print "reorder out cnt:",f.registers['hmc_vacc%i_reord_out_cnt'%vacc_n].read_uint()
    print "fifo wr cnt:",f.registers['hmc_vacc%i_fifo_wr_cnt'%vacc_n].read_uint()
    print "fifo rd cnt:",f.registers['hmc_vacc%i_fifo_rd_cnt'%vacc_n].read_uint()
    print "hmc wr cnt:",f.registers['hmc_vacc%i_hmc_wr_cnt'%vacc_n].read_uint()
    print "fifo out cnt:",f.registers['hmc_vacc%i_fifo_out_cnt'%vacc_n].read_uint()
    print "reorder miss cnt:",f.registers['hmc_vacc%i_reord_miss_cnt'%vacc_n].read_uint()
    print 'err status: ',f.registers['hmc_vacc%i_err_status'%vacc_n].read()['data']


print "HMC out snapshot stopped after %i valids."%(f.registers.hmc_vacc0_hmc_out_snap_ss_tr_en_cnt.read()['data']['reg']/8)
print "HMC in write snapshot stopped after %i valids."%(f.registers.hmc_vacc0_hmc_in_wr_snap_ss_tr_en_cnt.read()['data']['reg']/8)
print "HMC in read snapshot stopped after %i valids."%(f.registers.hmc_vacc0_hmc_in_wr_snap_ss_tr_en_cnt.read()['data']['reg']/8)
print "Reorder snapshot stopped after %i valids."%(f.registers.hmc_vacc0_qdr_out_snap_ss_tr_en_cnt.read()['data']['reg']/8)
print 'fifo status: ',f.registers.hmc_vacc0_fifo_status.read()['data']

#qdr=f.snapshots.hmc_vacc0_qdr_out_snap_ss.read(read_nowait=True)
#hmc=f.snapshots.hmc_vacc0_hmc_out_snap_ss.read(read_nowait=True)
#f.snapshots.hmc_vacc0_qdr_out_snap_ss.print_snap(read_nowait=True)
#f.snapshots.hmc_vacc0_ctrl_snap_ss.print_snap(read_nowait=True)
#f.snapshots.snap_acc.print_snap(read_nowait=True)
