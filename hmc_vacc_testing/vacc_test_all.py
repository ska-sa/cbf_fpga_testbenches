import casperfpga,time

f=casperfpga.SkarabFpga('10.99.55.170') # JRM board
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
#f.upload_to_ram_and_program('test_hmc_vacc_nosnap_2017-4-10_1530.fpg') #256b, 156MHz, Juri's flitgen mods, no serialiser
#f.upload_to_ram_and_program('test_hmc_vacc_all_2017-5-9_1318.fpg') #four vaccs, 225MHz. both interfaces on each hmc try to write to same memory locations and clobber each other. Can only test one interface at a time.
#f.upload_to_ram_and_program('test_hmc_vacc_all_2017-5-9_1544.fpg') #vector length: 1000
f.upload_to_ram_and_program('test_hmc_vacc_all_2017-5-11_1418.fpg') #vector length: 200000
print 'Programmed!'
f.registers.vacctvg_control.write(sync_sel=1,valid_sel=1,data_sel=1,ctr_en=1,vector_en=1,pulse_en=False)
#f.registers.vacctvg_control.write(reset='pulse')
f.registers.vacctvg_control.write(reset=1) #hold VACCs and TVGs in reset
f.registers.vacctvg_control.write(cnt_rst='pulse') #reset all counters to zero
time.sleep(1)
f.registers.vacctvg_control.write(reset=0) #bring VACC out of reset. TVG won't start yet
time.sleep(1)

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

print "READY TO START ACCUMULATING!"

#set the datarate:
#16/20 for 32Gbps at 156.25MHz
#14/20 for 28Gbps at 156.25 (minimum required performance for correlator's VACC)
#12/20 for 30.7Gbps at 200MHz (target bandwidth for normal correlator operation would be 10/20 at 235MHz=30.08Gbps)
#7/20 for 14Gbps at 156.25MHz (seems to be max lossless bandwidth with serialiser).
f.registers.vacc_tvg0_n_per_group.write(reg=1)
f.registers.vacc_tvg0_group_period.write(reg=200)
#f.registers.vacc_tvg1_n_per_group.write(reg=5)
#f.registers.vacc_tvg1_group_period.write(reg=20)
f.registers.vacc_tvg2_n_per_group.write(reg=5)
f.registers.vacc_tvg2_group_period.write(reg=20)
f.registers.vacc_tvg3_n_per_group.write(reg=5)
f.registers.vacc_tvg3_group_period.write(reg=20)

f.registers.acc_len.write(reg=3) #accumulate 200x 1000-length vectors.
f.registers.acc_len1.write(reg=3) #accumulate 200x 1000-length vectors.
f.registers.acc_len2.write(reg=3) #accumulate 200x 1000-length vectors.
f.registers.acc_len3.write(reg=3) #accumulate 200x 1000-length vectors.

f.registers.vacc_tvg0_n_pulses.write(reg=200e3*50*2+200e3) #generate 2 full accumulations, plus another single vector.
f.registers.vacc_tvg1_n_pulses.write(reg=200e3*50*2+200e3) #generate 2 full accumulations, plus another single vector.
f.registers.vacc_tvg2_n_pulses.write(reg=200e3*50*2+200e3) #generate 2 full accumulations, plus another single vector.
f.registers.vacc_tvg3_n_pulses.write(reg=200e3*50*2+200e3) #generate 2 full accumulations, plus another single vector.

f.registers.vacctvg_control.write(cnt_rst='pulse')

f.snapshots.snap_acc.arm(man_trig=True)
f.snapshots.snap_acc1.arm(man_trig=True)
f.snapshots.snap_acc2.arm(man_trig=True)
f.snapshots.snap_acc3.arm(man_trig=True)

print 'err status0: ',f.registers.hmc_vacc0_err_status.read()['data']
print 'err status1: ',f.registers.hmc_vacc1_err_status.read()['data']
print 'err status2: ',f.registers.hmc_vacc2_err_status.read()['data']
print 'err status3: ',f.registers.hmc_vacc3_err_status.read()['data']

#start the TVG running:
f.registers.vacctvg_control.write(reset=True,pulse_en=False)
f.registers.vacctvg_control.write(reset=False,pulse_en=True)
time.sleep(10)

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

