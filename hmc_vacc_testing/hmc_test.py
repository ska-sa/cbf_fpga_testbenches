import casperfpga,time

f=casperfpga.SkarabFpga('10.99.37.5')
f.upload_to_ram_and_program('test_hmc_2017-3-1_1149.fpg') #working!
#f.upload_to_ram_and_program('test_hmc_2017-2-27_0932.fpg') #working!

f.registers.wr_cntrl_n_pulses.write(reg=1000)
f.registers.wr_cntrl_n_per_group.write(reg=14)
f.registers.wr_cntrl_group_period.write(reg=20)

f.registers.rd_cntrl_n_pulses.write(reg=0)
f.registers.rd_cntrl_n_per_group.write(reg=14)
f.registers.rd_cntrl_group_period.write(reg=20)
f.registers.rd_cntrl_incr=1

time.sleep(0.1)
f.registers.rst.write(reg='pulse')
f.registers.vacctvg_control.write(sync_sel=1,valid_sel=1,data_sel=1,ctr_en=1)

#prep the snap block:
f.snapshots.hmc_in_snap_ss.arm(man_trig=True)
f.snapshots.hmc_out_snap_ss.arm(man_trig=True)

#start the TVG running:
f.registers.vacctvg_control.write(reset=False,pulse_en=False)
f.registers.vacctvg_control.write(reset=True,pulse_en=True)

time.sleep(1)
print "wr_req:",f.registers.hmc_wr_cnt.read_uint()
print "rd_req:",f.registers.hmc_rd_cnt.read_uint()
print "out:",f.registers.hmc_out_cnt.read_uint()

f.registers.rd_sel=2
f.registers.rd_cntrl_n_pulses.write(reg=1000)

print "wr_req:",f.registers.hmc_wr_cnt.read_uint()
print "rd_req:",f.registers.hmc_rd_cnt.read_uint()
print "out:",f.registers.hmc_out_cnt.read_uint()
