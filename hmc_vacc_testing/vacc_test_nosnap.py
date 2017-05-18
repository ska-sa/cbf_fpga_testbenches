import casperfpga,time

#f=casperfpga.SkarabFpga('10.99.55.170') #AvdB board
#f=casperfpga.SkarabFpga('10.99.51.170') #PP board
f=casperfpga.SkarabFpga('10.99.37.5') # JRM board
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-3-31_1045.fpg') #156.25MHz, div-by-4? readback/erase
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-3-31_0924.fpg') #180MHz, div-by-4? readback/erase
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-3-31_1640.fpg') #156.25MHz, div-by-16 readback/erase
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-3_0832.fpg') #180MHz, div-by-16 readback/erase
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-3_1218.fpg') #180MHz, div-by-16 readback/erase, 32B MAX BLOCK SIZE
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-3_1416.fpg') #200MHz, div-by-16, 32B, serialiser
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-3_1548.fpg') #156.25MHz, div-by-16, 32B, serialiser
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-3_1709.fpg') #as above, but with clean recompile
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-4_0932.fpg') #as above, but AvdB compile. None of above recent compiles worked. Board-specific POST troubles tracked to new resets.
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-4_1619.fpg') #156.25MHz, div-by-16, 32B, single AXI, some resets removed
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-4_1728.fpg') #156.25MHz, div-by-16, 32B, single AXI, no resets
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-5_1123.fpg') #As above, but 200MHz, DID NOT MAKE TIMING
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-6_0843.fpg') #256b VACC (4x31b numbers)
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-6_1109.fpg') #256b VACC (4x31b numbers), 156MHz, DIDNOTMAKETIMING
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-10_0946.fpg') #256b VACC (4x31b numbers), 156MHz, Juri's flitgen mods
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-10_1042.fpg') #256b VACC (4x31b numbers), 200MHz, Juri's flitgen mods
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-10_1433.fpg') #256b, 200MHz, Juri's flitgen mods, no serialiser
f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-10_1530.fpg') #256b, 156MHz, Juri's flitgen mods, no serialiser

f.registers.vacctvg_control.write(sync_sel=1,valid_sel=1,data_sel=1,ctr_en=1,vector_en=1)
#f.registers.vacctvg_control.write(reset='pulse')

#set the datarate:
#16/20 for 32Gbps at 156.25MHz
#14/20 for 28Gbps at 156.25 (minimum required performance for correlator's VACC)
#12/20 for 30.7Gbps at 200MHz (target bandwidth for normal correlator operation would be 10/20 at 235MHz=30.08Gbps)
#7/20 for 14Gbps at 156.25MHz (seems to be max lossless bandwidth with serialiser).
f.registers.vacc_tvg0_n_per_group.write(reg=16)
f.registers.vacc_tvg0_group_period.write(reg=20)

f.registers.acc_len.write(reg=200) #accumulate 200x 1000-length vectors.
f.registers.vacc_tvg0_n_pulses.write(reg=2001000) #generate 1 full accumulation, plus another single vector.

f.registers.hmc_vacc_cnt_rst.write(reg='pulse')
f.snapshots.snap_acc.arm(man_trig=True)

print 'err status: ',f.registers.hmc_vacc_err_status.read()['data']

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

print 'err status: ',f.registers.hmc_vacc_err_status.read()['data']

