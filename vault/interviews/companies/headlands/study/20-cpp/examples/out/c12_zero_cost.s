	.build_version macos, 27, 0	sdk_version 27, 0
	.section	__TEXT,__text,regular,pure_instructions
	.globl	__Z7sum_rawPKim                 ; -- Begin function _Z7sum_rawPKim
	.p2align	2
__Z7sum_rawPKim:                        ; @_Z7sum_rawPKim
	.cfi_startproc
; %bb.0:
	cbz	x1, LBB0_3
; %bb.1:
	cmp	x1, #3
	b.hi	LBB0_4
; %bb.2:
	mov	x9, #0                          ; =0x0
	mov	x8, #0                          ; =0x0
	b	LBB0_13
LBB0_3:
	mov	x8, #0                          ; =0x0
	mov	x0, x8
	ret
LBB0_4:
	cmp	x1, #16
	b.hs	LBB0_6
; %bb.5:
	mov	x9, #0                          ; =0x0
	mov	x8, #0                          ; =0x0
	b	LBB0_10
LBB0_6:
	movi.2d	v0, #0000000000000000
	and	x9, x1, #0xfffffffffffffff0
	movi.2d	v1, #0000000000000000
	add	x8, x0, #32
	mov	x10, x9
	movi.2d	v3, #0000000000000000
	movi.2d	v4, #0000000000000000
	movi.2d	v5, #0000000000000000
	movi.2d	v2, #0000000000000000
	movi.2d	v7, #0000000000000000
	movi.2d	v6, #0000000000000000
LBB0_7:                                 ; =>This Inner Loop Header: Depth=1
	ldp	q16, q17, [x8, #-32]
	saddw2.2d	v1, v1, v16
	saddw.2d	v0, v0, v16
	ldp	q16, q18, [x8], #64
	saddw2.2d	v4, v4, v17
	saddw.2d	v3, v3, v17
	saddw2.2d	v2, v2, v16
	saddw.2d	v5, v5, v16
	saddw2.2d	v6, v6, v18
	saddw.2d	v7, v7, v18
	subs	x10, x10, #16
	b.ne	LBB0_7
; %bb.8:
	add.2d	v0, v3, v0
	add.2d	v1, v4, v1
	add.2d	v3, v7, v5
	add.2d	v0, v3, v0
	add.2d	v2, v6, v2
	add.2d	v1, v2, v1
	add.2d	v0, v0, v1
	addp.2d	d0, v0
	fmov	x8, d0
	cmp	x1, x9
	b.eq	LBB0_15
; %bb.9:
	tst	x1, #0xc
	b.eq	LBB0_13
LBB0_10:
	mov	x10, x9
	and	x9, x1, #0xfffffffffffffffc
	movi.2d	v0, #0000000000000000
	movi.2d	v1, #0000000000000000
	mov.d	v1[0], x8
	sub	x8, x10, x9
	add	x10, x0, x10, lsl #2
LBB0_11:                                ; =>This Inner Loop Header: Depth=1
	ldr	q2, [x10], #16
	saddw2.2d	v0, v0, v2
	saddw.2d	v1, v1, v2
	adds	x8, x8, #4
	b.ne	LBB0_11
; %bb.12:
	add.2d	v0, v1, v0
	addp.2d	d0, v0
	fmov	x8, d0
	cmp	x1, x9
	b.eq	LBB0_15
LBB0_13:
	sub	x10, x1, x9
	add	x9, x0, x9, lsl #2
LBB0_14:                                ; =>This Inner Loop Header: Depth=1
	ldrsw	x11, [x9], #4
	add	x8, x8, x11
	subs	x10, x10, #1
	b.ne	LBB0_14
LBB0_15:
	mov	x0, x8
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	__Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE ; -- Begin function _Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE
	.p2align	2
__Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE: ; @_Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE
	.cfi_startproc
; %bb.0:
	ldp	x10, x8, [x0]
	cmp	x10, x8
	b.eq	LBB1_3
; %bb.1:
	sub	x9, x8, x10
	sub	x11, x9, #4
	cmp	x11, #12
	b.hs	LBB1_4
; %bb.2:
	mov	x0, #0                          ; =0x0
	mov	x12, x10
	b	LBB1_15
LBB1_3:
	mov	x0, #0                          ; =0x0
	ret
LBB1_4:
	lsr	x9, x11, #2
	add	x9, x9, #1
	cmp	x11, #60
	b.hs	LBB1_6
; %bb.5:
	mov	x11, #0                         ; =0x0
	mov	x0, #0                          ; =0x0
	b	LBB1_10
LBB1_6:
	movi.2d	v0, #0000000000000000
	and	x11, x9, #0x7ffffffffffffff0
	movi.2d	v1, #0000000000000000
	add	x12, x10, #32
	mov	x13, x11
	movi.2d	v3, #0000000000000000
	movi.2d	v4, #0000000000000000
	movi.2d	v5, #0000000000000000
	movi.2d	v2, #0000000000000000
	movi.2d	v7, #0000000000000000
	movi.2d	v6, #0000000000000000
LBB1_7:                                 ; =>This Inner Loop Header: Depth=1
	ldp	q16, q17, [x12, #-32]
	saddw2.2d	v1, v1, v16
	saddw.2d	v0, v0, v16
	ldp	q16, q18, [x12], #64
	saddw2.2d	v4, v4, v17
	saddw.2d	v3, v3, v17
	saddw2.2d	v2, v2, v16
	saddw.2d	v5, v5, v16
	saddw2.2d	v6, v6, v18
	saddw.2d	v7, v7, v18
	subs	x13, x13, #16
	b.ne	LBB1_7
; %bb.8:
	add.2d	v0, v3, v0
	add.2d	v1, v4, v1
	add.2d	v3, v7, v5
	add.2d	v0, v3, v0
	add.2d	v2, v6, v2
	add.2d	v1, v2, v1
	add.2d	v0, v0, v1
	addp.2d	d0, v0
	fmov	x0, d0
	cmp	x9, x11
	b.eq	LBB1_13
; %bb.9:
	tst	x9, #0xc
	b.eq	LBB1_14
LBB1_10:
	and	x13, x9, #0x7ffffffffffffffc
	add	x12, x10, x13, lsl #2
	movi.2d	v0, #0000000000000000
	movi.2d	v1, #0000000000000000
	mov.d	v1[0], x0
	add	x10, x10, x11, lsl #2
	sub	x11, x11, x13
LBB1_11:                                ; =>This Inner Loop Header: Depth=1
	ldr	q2, [x10], #16
	saddw2.2d	v0, v0, v2
	saddw.2d	v1, v1, v2
	adds	x11, x11, #4
	b.ne	LBB1_11
; %bb.12:
	add.2d	v0, v1, v0
	addp.2d	d0, v0
	fmov	x0, d0
	cmp	x9, x13
	b.ne	LBB1_15
LBB1_13:
	ret
LBB1_14:
	add	x12, x10, x11, lsl #2
LBB1_15:                                ; =>This Inner Loop Header: Depth=1
	ldrsw	x9, [x12], #4
	add	x0, x0, x9
	cmp	x12, x8
	b.ne	LBB1_15
	b	LBB1_13
	.cfi_endproc
                                        ; -- End function
	.globl	__Z12sum_rangeforRKNSt3__16vectorIiNS_9allocatorIiEEEE ; -- Begin function _Z12sum_rangeforRKNSt3__16vectorIiNS_9allocatorIiEEEE
	.p2align	2
__Z12sum_rangeforRKNSt3__16vectorIiNS_9allocatorIiEEEE: ; @_Z12sum_rangeforRKNSt3__16vectorIiNS_9allocatorIiEEEE
	.cfi_startproc
; %bb.0:
	ldp	x10, x8, [x0]
	cmp	x10, x8
	b.eq	LBB2_3
; %bb.1:
	sub	x9, x8, x10
	sub	x11, x9, #4
	cmp	x11, #11
	b.hi	LBB2_4
; %bb.2:
	mov	x0, #0                          ; =0x0
	mov	x12, x10
	b	LBB2_15
LBB2_3:
	mov	x0, #0                          ; =0x0
	ret
LBB2_4:
	lsr	x9, x11, #2
	add	x9, x9, #1
	cmp	x11, #60
	b.hs	LBB2_6
; %bb.5:
	mov	x11, #0                         ; =0x0
	mov	x0, #0                          ; =0x0
	b	LBB2_10
LBB2_6:
	movi.2d	v0, #0000000000000000
	and	x11, x9, #0x7ffffffffffffff0
	movi.2d	v1, #0000000000000000
	add	x12, x10, #32
	mov	x13, x11
	movi.2d	v3, #0000000000000000
	movi.2d	v4, #0000000000000000
	movi.2d	v5, #0000000000000000
	movi.2d	v2, #0000000000000000
	movi.2d	v7, #0000000000000000
	movi.2d	v6, #0000000000000000
LBB2_7:                                 ; =>This Inner Loop Header: Depth=1
	ldp	q16, q17, [x12, #-32]
	saddw2.2d	v1, v1, v16
	saddw.2d	v0, v0, v16
	ldp	q16, q18, [x12], #64
	saddw2.2d	v4, v4, v17
	saddw.2d	v3, v3, v17
	saddw2.2d	v2, v2, v16
	saddw.2d	v5, v5, v16
	saddw2.2d	v6, v6, v18
	saddw.2d	v7, v7, v18
	subs	x13, x13, #16
	b.ne	LBB2_7
; %bb.8:
	add.2d	v0, v3, v0
	add.2d	v1, v4, v1
	add.2d	v3, v7, v5
	add.2d	v0, v3, v0
	add.2d	v2, v6, v2
	add.2d	v1, v2, v1
	add.2d	v0, v0, v1
	addp.2d	d0, v0
	fmov	x0, d0
	cmp	x9, x11
	b.eq	LBB2_13
; %bb.9:
	tst	x9, #0xc
	b.eq	LBB2_14
LBB2_10:
	and	x13, x9, #0x7ffffffffffffffc
	add	x12, x10, x13, lsl #2
	movi.2d	v0, #0000000000000000
	movi.2d	v1, #0000000000000000
	mov.d	v1[0], x0
	add	x10, x10, x11, lsl #2
	sub	x11, x11, x13
LBB2_11:                                ; =>This Inner Loop Header: Depth=1
	ldr	q2, [x10], #16
	saddw2.2d	v0, v0, v2
	saddw.2d	v1, v1, v2
	adds	x11, x11, #4
	b.ne	LBB2_11
; %bb.12:
	add.2d	v0, v1, v0
	addp.2d	d0, v0
	fmov	x0, d0
	cmp	x9, x13
	b.ne	LBB2_15
LBB2_13:
	ret
LBB2_14:
	add	x12, x10, x11, lsl #2
LBB2_15:                                ; =>This Inner Loop Header: Depth=1
	ldrsw	x9, [x12], #4
	add	x0, x0, x9
	cmp	x12, x8
	b.ne	LBB2_15
	b	LBB2_13
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
Lfunc_begin0:
	.cfi_startproc
	.cfi_personality 155, ___gxx_personality_v0
	.cfi_lsda 16, Lexception0
; %bb.0:
	stp	d9, d8, [sp, #-112]!            ; 16-byte Folded Spill
	stp	x28, x27, [sp, #16]             ; 16-byte Folded Spill
	stp	x26, x25, [sp, #32]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #48]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #64]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #80]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #96]             ; 16-byte Folded Spill
	add	x29, sp, #96
	sub	sp, sp, #2560
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	.cfi_offset w27, -88
	.cfi_offset w28, -96
	.cfi_offset b8, -104
	.cfi_offset b9, -112
Lloh0:
	adrp	x0, l_.str@PAGE
Lloh1:
	add	x0, x0, l_.str@PAGEOFF
	bl	_getenv
	mov	w8, #11                         ; =0xb
	str	w8, [sp, #40]
	mov	w9, #1                          ; =0x1
	mov	w10, #35173                     ; =0x8965
	movk	w10, #27655, lsl #16
	add	x11, sp, #40
LBB3_1:                                 ; =>This Inner Loop Header: Depth=1
	eor	w8, w8, w8, lsr #30
	madd	w8, w8, w10, w9
	str	w8, [x11, x9, lsl #2]
	add	x9, x9, #1
	cmp	x9, #624
	b.ne	LBB3_1
; %bb.2:
	mov	w8, #34464                      ; =0x86a0
	movk	w8, #1, lsl #16
	mov	w9, #19264                      ; =0x4b40
	movk	w9, #76, lsl #16
	cmp	x0, #0
	csel	x24, x9, x8, eq
	lsl	x20, x24, #2
	mov	x0, x20
	bl	__Znwm
	mov	x19, x0
	add	x21, x0, x20
	str	x0, [sp, #16]
	str	x21, [sp, #32]
	mov	x1, x20
	bl	_bzero
	mov	x8, #0                          ; =0x0
	mov	x17, #0                         ; =0x0
	str	x21, [sp, #24]
	add	x9, sp, #40
	mov	x10, #3361                      ; =0xd21
	movk	x10, #8402, lsl #16
	movk	x10, #53773, lsl #32
	movk	x10, #3360, lsl #48
	mov	w11, #624                       ; =0x270
	mov	w12, #45279                     ; =0xb0df
	movk	w12, #39176, lsl #16
	mov	w13, #22144                     ; =0x5680
	movk	w13, #40236, lsl #16
	mov	w14, #-272236544                ; =0xefc60000
	mov	w15, #56963                     ; =0xde83
	movk	w15, #17179, lsl #16
	mov	w16, #16960                     ; =0x4240
	movk	w16, #15, lsl #16
LBB3_3:                                 ; =>This Inner Loop Header: Depth=1
	add	x0, x17, #1
	cmp	x0, #624
	csinc	x0, xzr, x17, eq
	ldr	w1, [x9, x17, lsl #2]
	ldr	w2, [x9, x0, lsl #2]
	and	w1, w1, #0x80000000
	and	w3, w2, #0x7ffffffe
	orr	w1, w3, w1
	add	x3, x17, #397
	lsr	x4, x3, #4
	umulh	x4, x4, x10
	lsr	x4, x4, #1
	msub	x3, x4, x11, x3
	ldr	w3, [x9, x3, lsl #2]
	tst	w2, #0x1
	csel	w2, w12, wzr, ne
	eor	w2, w2, w3
	eor	w1, w2, w1, lsr #1
	str	w1, [x9, x17, lsl #2]
	eor	w17, w1, w1, lsr #11
	and	w1, w13, w17, lsl #7
	eor	w17, w1, w17
	and	w1, w14, w17, lsl #15
	eor	w17, w1, w17
	eor	w17, w17, w17, lsr #18
	umull	x1, w17, w15
	lsr	x1, x1, #50
	msub	w17, w1, w16, w17
	str	w17, [x19, x8]
	add	x8, x8, #4
	mov	x17, x0
	cmp	x20, x8
	b.ne	LBB3_3
; %bb.4:
Ltmp0:
Lloh2:
	adrp	x0, __ZNSt3__14coutE@GOTPAGE
Lloh3:
	ldr	x0, [x0, __ZNSt3__14coutE@GOTPAGEOFF]
Lloh4:
	adrp	x1, l_.str.1@PAGE
Lloh5:
	add	x1, x1, l_.str.1@PAGEOFF
	mov	w2, #12                         ; =0xc
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp1:
; %bb.5:
	mov	x21, x0
	mov	x0, x19
	mov	x1, x24
	bl	__Z7sum_rawPKim
	mov	x22, x0
	add	x0, sp, #16
	bl	__Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE
	cmp	x22, x0
	b.ne	LBB3_7
; %bb.6:
	add	x0, sp, #16
	bl	__Z14sum_accumulateRKNSt3__16vectorIiNS_9allocatorIiEEEE
	mov	x22, x0
	add	x0, sp, #16
	bl	__Z12sum_rangeforRKNSt3__16vectorIiNS_9allocatorIiEEEE
	cmp	x22, x0
	cset	w1, eq
	b	LBB3_8
LBB3_7:
	mov	w1, #0                          ; =0x0
LBB3_8:
Ltmp2:
	mov	x0, x21
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEb
Ltmp3:
; %bb.9:
Ltmp4:
Lloh6:
	adrp	x1, l_.str.2@PAGE
Lloh7:
	add	x1, x1, l_.str.2@PAGEOFF
	mov	w2, #1                          ; =0x1
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp5:
; %bb.10:
Ltmp7:
	mov	x0, x20
	bl	__Znwm
Ltmp8:
; %bb.11:
	mov	x21, x0
	mov	x1, x19
	mov	x2, x20
	bl	_memcpy
Ltmp10:
	mov	x0, x20
	bl	__Znwm
Ltmp11:
; %bb.12:
	mov	x22, x0
	mov	x1, x19
	mov	x2, x20
	bl	_memcpy
Ltmp13:
	mov	x0, x20
	bl	__Znwm
Ltmp14:
; %bb.13:
	mov	x27, x0
	mov	x1, x19
	mov	x2, x20
	bl	_memcpy
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	mov	x28, x0
Ltmp16:
	add	x1, x21, x20
	sub	x2, x29, #105
	mov	x0, x21
	str	x27, [sp, #8]                   ; 8-byte Folded Spill
	bl	__ZNSt3__16__sortIRNS_6__lessIiiEEPiEEvT0_S5_T_
Ltmp17:
; %bb.14:
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	mov	x25, x0
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	mov	x26, x0
	clz	x8, x24
	lsl	x8, x8, #1
	add	x1, x22, x20
	eor	x2, x8, #0x7e
	mov	x0, x22
	mov	w3, #1                          ; =0x1
	bl	__ZNSt3__111__introsortINS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiLb0EEEvT1_S6_T0_NS_15iterator_traitsIS6_E15difference_typeEb
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	mov	x23, x0
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	str	x0, [sp]                        ; 8-byte Folded Spill
Ltmp19:
Lloh8:
	adrp	x3, __ZL7cmp_intPKvS0_@PAGE
Lloh9:
	add	x3, x3, __ZL7cmp_intPKvS0_@PAGEOFF
	mov	x0, x27
	mov	x1, x24
	mov	w2, #4                          ; =0x4
	bl	_qsort
Ltmp20:
; %bb.15:
	bl	__ZNSt3__16chrono12steady_clock3nowEv
	mov	x27, x0
Ltmp22:
Lloh10:
	adrp	x0, __ZNSt3__14coutE@GOTPAGE
Lloh11:
	ldr	x0, [x0, __ZNSt3__14coutE@GOTPAGEOFF]
Lloh12:
	adrp	x1, l_.str.3@PAGE
Lloh13:
	add	x1, x1, l_.str.3@PAGEOFF
	mov	w2, #5                          ; =0x5
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp23:
; %bb.16:
Ltmp24:
	mov	x1, x24
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEm
Ltmp25:
; %bb.17:
Ltmp26:
Lloh14:
	adrp	x1, l_.str.4@PAGE
Lloh15:
	add	x1, x1, l_.str.4@PAGEOFF
	mov	w2, #18                         ; =0x12
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp27:
; %bb.18:
Ltmp28:
	sub	x8, x25, x28
	scvtf	d0, x8
	mov	x8, #145685290680320            ; =0x848000000000
	movk	x8, #16686, lsl #48
	fmov	d9, x8
	fdiv	d8, d0, d9
	mov.16b	v0, v8
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEd
Ltmp29:
; %bb.19:
Ltmp30:
Lloh16:
	adrp	x1, l_.str.5@PAGE
Lloh17:
	add	x1, x1, l_.str.5@PAGEOFF
	mov	w2, #25                         ; =0x19
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp31:
; %bb.20:
Ltmp32:
	sub	x8, x23, x26
	scvtf	d0, x8
	fdiv	d0, d0, d9
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEd
Ltmp33:
; %bb.21:
Ltmp34:
Lloh18:
	adrp	x1, l_.str.6@PAGE
Lloh19:
	add	x1, x1, l_.str.6@PAGEOFF
	mov	w2, #12                         ; =0xc
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp35:
; %bb.22:
Ltmp36:
	ldr	x8, [sp]                        ; 8-byte Folded Reload
	sub	x8, x27, x8
	scvtf	d0, x8
	mov	x8, #145685290680320            ; =0x848000000000
	movk	x8, #16686, lsl #48
	fmov	d1, x8
	fdiv	d9, d0, d1
	mov.16b	v0, v9
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEd
Ltmp37:
; %bb.23:
Ltmp38:
Lloh20:
	adrp	x1, l_.str.7@PAGE
Lloh21:
	add	x1, x1, l_.str.7@PAGEOFF
	mov	w2, #23                         ; =0x17
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp39:
; %bb.24:
	fdiv	d0, d9, d8
Ltmp40:
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEd
Ltmp41:
; %bb.25:
Ltmp42:
Lloh22:
	adrp	x1, l_.str.8@PAGE
Lloh23:
	add	x1, x1, l_.str.8@PAGEOFF
	mov	w2, #3                          ; =0x3
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp43:
; %bb.26:
Ltmp44:
Lloh24:
	adrp	x0, __ZNSt3__14coutE@GOTPAGE
Lloh25:
	ldr	x0, [x0, __ZNSt3__14coutE@GOTPAGEOFF]
Lloh26:
	adrp	x1, l_.str.9@PAGE
Lloh27:
	add	x1, x1, l_.str.9@PAGEOFF
	mov	w2, #19                         ; =0x13
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp45:
; %bb.27:
	mov	x23, x0
	mov	x0, x21
	mov	x1, x22
	mov	x2, x20
	bl	_memcmp
	cbz	w0, LBB3_29
; %bb.28:
	mov	w1, #0                          ; =0x0
	b	LBB3_30
LBB3_29:
	mov	x0, x22
	ldr	x1, [sp, #8]                    ; 8-byte Folded Reload
	mov	x2, x20
	bl	_memcmp
	cmp	w0, #0
	cset	w1, eq
LBB3_30:
Ltmp46:
	mov	x0, x23
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEb
Ltmp47:
; %bb.31:
Ltmp48:
Lloh28:
	adrp	x1, l_.str.2@PAGE
Lloh29:
	add	x1, x1, l_.str.2@PAGEOFF
	mov	w2, #1                          ; =0x1
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp49:
; %bb.32:
	ldr	x0, [sp, #8]                    ; 8-byte Folded Reload
	bl	__ZdlPv
	mov	x0, x22
	bl	__ZdlPv
	mov	x0, x21
	bl	__ZdlPv
	mov	x0, x19
	bl	__ZdlPv
	mov	w0, #0                          ; =0x0
	add	sp, sp, #2560
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #80]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #64]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #48]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #32]             ; 16-byte Folded Reload
	ldp	x28, x27, [sp, #16]             ; 16-byte Folded Reload
	ldp	d9, d8, [sp], #112              ; 16-byte Folded Reload
	ret
LBB3_33:
Ltmp21:
	b	LBB3_40
LBB3_34:
Ltmp18:
	b	LBB3_40
LBB3_35:
Ltmp15:
	mov	x20, x0
	b	LBB3_41
LBB3_36:
Ltmp12:
	mov	x20, x0
	b	LBB3_42
LBB3_37:
Ltmp9:
	mov	x20, x0
	b	LBB3_43
LBB3_38:
Ltmp6:
	mov	x20, x0
	b	LBB3_43
LBB3_39:
Ltmp50:
LBB3_40:
	mov	x20, x0
	ldr	x0, [sp, #8]                    ; 8-byte Folded Reload
	bl	__ZdlPv
LBB3_41:
	mov	x0, x22
	bl	__ZdlPv
LBB3_42:
	mov	x0, x21
	bl	__ZdlPv
LBB3_43:
	mov	x0, x19
	bl	__ZdlPv
	mov	x0, x20
	bl	__Unwind_Resume
	.loh AdrpAdd	Lloh0, Lloh1
	.loh AdrpAdd	Lloh4, Lloh5
	.loh AdrpLdrGot	Lloh2, Lloh3
	.loh AdrpAdd	Lloh6, Lloh7
	.loh AdrpAdd	Lloh8, Lloh9
	.loh AdrpAdd	Lloh12, Lloh13
	.loh AdrpLdrGot	Lloh10, Lloh11
	.loh AdrpAdd	Lloh14, Lloh15
	.loh AdrpAdd	Lloh16, Lloh17
	.loh AdrpAdd	Lloh18, Lloh19
	.loh AdrpAdd	Lloh20, Lloh21
	.loh AdrpAdd	Lloh22, Lloh23
	.loh AdrpAdd	Lloh26, Lloh27
	.loh AdrpLdrGot	Lloh24, Lloh25
	.loh AdrpAdd	Lloh28, Lloh29
Lfunc_end0:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table3:
Lexception0:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	255                             ; @TType Encoding = omit
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end0-Lcst_begin0
Lcst_begin0:
	.uleb128 Lfunc_begin0-Lfunc_begin0      ; >> Call Site 1 <<
	.uleb128 Ltmp0-Lfunc_begin0             ;   Call between Lfunc_begin0 and Ltmp0
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp0-Lfunc_begin0             ; >> Call Site 2 <<
	.uleb128 Ltmp5-Ltmp0                    ;   Call between Ltmp0 and Ltmp5
	.uleb128 Ltmp6-Lfunc_begin0             ;     jumps to Ltmp6
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp7-Lfunc_begin0             ; >> Call Site 3 <<
	.uleb128 Ltmp8-Ltmp7                    ;   Call between Ltmp7 and Ltmp8
	.uleb128 Ltmp9-Lfunc_begin0             ;     jumps to Ltmp9
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp8-Lfunc_begin0             ; >> Call Site 4 <<
	.uleb128 Ltmp10-Ltmp8                   ;   Call between Ltmp8 and Ltmp10
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp10-Lfunc_begin0            ; >> Call Site 5 <<
	.uleb128 Ltmp11-Ltmp10                  ;   Call between Ltmp10 and Ltmp11
	.uleb128 Ltmp12-Lfunc_begin0            ;     jumps to Ltmp12
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp11-Lfunc_begin0            ; >> Call Site 6 <<
	.uleb128 Ltmp13-Ltmp11                  ;   Call between Ltmp11 and Ltmp13
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp13-Lfunc_begin0            ; >> Call Site 7 <<
	.uleb128 Ltmp14-Ltmp13                  ;   Call between Ltmp13 and Ltmp14
	.uleb128 Ltmp15-Lfunc_begin0            ;     jumps to Ltmp15
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp14-Lfunc_begin0            ; >> Call Site 8 <<
	.uleb128 Ltmp16-Ltmp14                  ;   Call between Ltmp14 and Ltmp16
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp16-Lfunc_begin0            ; >> Call Site 9 <<
	.uleb128 Ltmp17-Ltmp16                  ;   Call between Ltmp16 and Ltmp17
	.uleb128 Ltmp18-Lfunc_begin0            ;     jumps to Ltmp18
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp19-Lfunc_begin0            ; >> Call Site 10 <<
	.uleb128 Ltmp20-Ltmp19                  ;   Call between Ltmp19 and Ltmp20
	.uleb128 Ltmp21-Lfunc_begin0            ;     jumps to Ltmp21
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp22-Lfunc_begin0            ; >> Call Site 11 <<
	.uleb128 Ltmp49-Ltmp22                  ;   Call between Ltmp22 and Ltmp49
	.uleb128 Ltmp50-Lfunc_begin0            ;     jumps to Ltmp50
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp49-Lfunc_begin0            ; >> Call Site 12 <<
	.uleb128 Lfunc_end0-Ltmp49              ;   Call between Ltmp49 and Lfunc_end0
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
Lcst_end0:
	.p2align	2, 0x0
                                        ; -- End function
	.section	__TEXT,__text,regular,pure_instructions
	.private_extern	___clang_call_terminate ; -- Begin function __clang_call_terminate
	.globl	___clang_call_terminate
	.weak_def_can_be_hidden	___clang_call_terminate
	.p2align	2
___clang_call_terminate:                ; @__clang_call_terminate
	.cfi_startproc
; %bb.0:
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	bl	___cxa_begin_catch
	bl	__ZSt9terminatev
	.cfi_endproc
                                        ; -- End function
	.private_extern	__ZNSt3__120__throw_length_errorB9nqe220106EPKc ; -- Begin function _ZNSt3__120__throw_length_errorB9nqe220106EPKc
	.globl	__ZNSt3__120__throw_length_errorB9nqe220106EPKc
	.weak_def_can_be_hidden	__ZNSt3__120__throw_length_errorB9nqe220106EPKc
	.p2align	2
__ZNSt3__120__throw_length_errorB9nqe220106EPKc: ; @_ZNSt3__120__throw_length_errorB9nqe220106EPKc
Lfunc_begin1:
	.cfi_startproc
	.cfi_personality 155, ___gxx_personality_v0
	.cfi_lsda 16, Lexception1
; %bb.0:
	stp	x20, x19, [sp, #-32]!           ; 16-byte Folded Spill
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	mov	x20, x0
	mov	w0, #16                         ; =0x10
	bl	___cxa_allocate_exception
	mov	x19, x0
Ltmp51:
	mov	x1, x20
	bl	__ZNSt12length_errorC1B9nqe220106EPKc
Ltmp52:
; %bb.1:
Lloh30:
	adrp	x1, __ZTISt12length_error@GOTPAGE
Lloh31:
	ldr	x1, [x1, __ZTISt12length_error@GOTPAGEOFF]
Lloh32:
	adrp	x2, __ZNSt12length_errorD1Ev@GOTPAGE
Lloh33:
	ldr	x2, [x2, __ZNSt12length_errorD1Ev@GOTPAGEOFF]
	mov	x0, x19
	bl	___cxa_throw
LBB5_2:
Ltmp53:
	mov	x20, x0
	mov	x0, x19
	bl	___cxa_free_exception
	mov	x0, x20
	bl	__Unwind_Resume
	.loh AdrpLdrGot	Lloh32, Lloh33
	.loh AdrpLdrGot	Lloh30, Lloh31
Lfunc_end1:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table5:
Lexception1:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	255                             ; @TType Encoding = omit
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end1-Lcst_begin1
Lcst_begin1:
	.uleb128 Lfunc_begin1-Lfunc_begin1      ; >> Call Site 1 <<
	.uleb128 Ltmp51-Lfunc_begin1            ;   Call between Lfunc_begin1 and Ltmp51
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp51-Lfunc_begin1            ; >> Call Site 2 <<
	.uleb128 Ltmp52-Ltmp51                  ;   Call between Ltmp51 and Ltmp52
	.uleb128 Ltmp53-Lfunc_begin1            ;     jumps to Ltmp53
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp52-Lfunc_begin1            ; >> Call Site 3 <<
	.uleb128 Lfunc_end1-Ltmp52              ;   Call between Ltmp52 and Lfunc_end1
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
Lcst_end1:
	.p2align	2, 0x0
                                        ; -- End function
	.section	__TEXT,__text,regular,pure_instructions
	.private_extern	__ZNSt12length_errorC1B9nqe220106EPKc ; -- Begin function _ZNSt12length_errorC1B9nqe220106EPKc
	.globl	__ZNSt12length_errorC1B9nqe220106EPKc
	.weak_def_can_be_hidden	__ZNSt12length_errorC1B9nqe220106EPKc
	.p2align	2
__ZNSt12length_errorC1B9nqe220106EPKc:  ; @_ZNSt12length_errorC1B9nqe220106EPKc
	.cfi_startproc
; %bb.0:
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	bl	__ZNSt11logic_errorC2EPKc
Lloh34:
	adrp	x8, __ZTVSt12length_error@GOTPAGE
Lloh35:
	ldr	x8, [x8, __ZTVSt12length_error@GOTPAGEOFF]
	add	x8, x8, #16
	str	x8, [x0]
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.loh AdrpLdrGot	Lloh34, Lloh35
	.cfi_endproc
                                        ; -- End function
	.p2align	2                               ; -- Begin function _ZNSt3__111__introsortINS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiLb0EEEvT1_S6_T0_NS_15iterator_traitsIS6_E15difference_typeEb
__ZNSt3__111__introsortINS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiLb0EEEvT1_S6_T0_NS_15iterator_traitsIS6_E15difference_typeEb: ; @"_ZNSt3__111__introsortINS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiLb0EEEvT1_S6_T0_NS_15iterator_traitsIS6_E15difference_typeEb"
	.cfi_startproc
; %bb.0:
	stp	x26, x25, [sp, #-80]!           ; 16-byte Folded Spill
	stp	x24, x23, [sp, #16]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #32]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #48]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #64]             ; 16-byte Folded Spill
	add	x29, sp, #64
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	mov	x22, x3
	mov	x21, x2
	mov	x20, x1
	mov	x19, x0
LBB7_1:                                 ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB7_2 Depth 2
                                        ;       Child Loop BB7_84 Depth 3
                                        ;       Child Loop BB7_82 Depth 3
                                        ;       Child Loop BB7_88 Depth 3
                                        ;       Child Loop BB7_91 Depth 3
                                        ;         Child Loop BB7_92 Depth 4
                                        ;         Child Loop BB7_93 Depth 4
                                        ;       Child Loop BB7_61 Depth 3
                                        ;       Child Loop BB7_63 Depth 3
                                        ;       Child Loop BB7_65 Depth 3
                                        ;       Child Loop BB7_69 Depth 3
                                        ;         Child Loop BB7_70 Depth 4
                                        ;         Child Loop BB7_71 Depth 4
	mov	x23, x19
LBB7_2:                                 ;   Parent Loop BB7_1 Depth=1
                                        ; =>  This Loop Header: Depth=2
                                        ;       Child Loop BB7_84 Depth 3
                                        ;       Child Loop BB7_82 Depth 3
                                        ;       Child Loop BB7_88 Depth 3
                                        ;       Child Loop BB7_91 Depth 3
                                        ;         Child Loop BB7_92 Depth 4
                                        ;         Child Loop BB7_93 Depth 4
                                        ;       Child Loop BB7_61 Depth 3
                                        ;       Child Loop BB7_63 Depth 3
                                        ;       Child Loop BB7_65 Depth 3
                                        ;       Child Loop BB7_69 Depth 3
                                        ;         Child Loop BB7_70 Depth 4
                                        ;         Child Loop BB7_71 Depth 4
	mov	x19, x23
	sub	x10, x20, x23
	asr	x8, x10, #2
	subs	x9, x8, #2
	b.gt	LBB7_5
; %bb.3:                                ;   in Loop: Header=BB7_2 Depth=2
	b.lo	LBB7_187
; %bb.4:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	x8, #2
	b.ne	LBB7_8
	b	LBB7_102
LBB7_5:                                 ;   in Loop: Header=BB7_2 Depth=2
	cmp	x8, #3
	b.eq	LBB7_104
; %bb.6:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	x8, #4
	b.eq	LBB7_107
; %bb.7:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	x8, #5
	b.eq	LBB7_99
LBB7_8:                                 ;   in Loop: Header=BB7_2 Depth=2
	cmp	x8, #23
	b.le	LBB7_110
; %bb.9:                                ;   in Loop: Header=BB7_2 Depth=2
	cbz	x21, LBB7_120
; %bb.10:                               ;   in Loop: Header=BB7_2 Depth=2
	lsr	x9, x8, #1
	add	x9, x19, x9, lsl #2
	ldur	w10, [x20, #-4]
	cmp	x8, #129
	b.lo	LBB7_14
; %bb.11:                               ;   in Loop: Header=BB7_2 Depth=2
	ldr	w11, [x9]
	ldr	w8, [x19]
	cmp	w11, w8
	b.ge	LBB7_17
; %bb.12:                               ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_23
; %bb.13:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x19]
	b	LBB7_25
LBB7_14:                                ;   in Loop: Header=BB7_2 Depth=2
	ldr	w11, [x19]
	ldr	w8, [x9]
	cmp	w11, w8
	b.ge	LBB7_20
; %bb.15:                               ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_32
; %bb.16:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x9]
	b	LBB7_34
LBB7_17:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_26
; %bb.18:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x9]
	stur	w11, [x20, #-4]
	ldr	w8, [x9]
	ldr	w10, [x19]
	cmp	w8, w10
	b.ge	LBB7_26
; %bb.19:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w8, [x19]
	str	w10, [x9]
	b	LBB7_26
LBB7_20:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_58
; %bb.21:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x19]
	stur	w11, [x20, #-4]
	ldr	w8, [x19]
	ldr	w10, [x9]
	cmp	w8, w10
	b.ge	LBB7_58
; %bb.22:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w8, [x9]
	str	w10, [x19]
	b	LBB7_58
LBB7_23:                                ;   in Loop: Header=BB7_2 Depth=2
	str	w11, [x19]
	str	w8, [x9]
	ldur	w10, [x20, #-4]
	cmp	w10, w8
	b.ge	LBB7_26
; %bb.24:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x9]
LBB7_25:                                ;   in Loop: Header=BB7_2 Depth=2
	stur	w8, [x20, #-4]
LBB7_26:                                ;   in Loop: Header=BB7_2 Depth=2
	ldur	w10, [x9, #-4]
	ldr	w8, [x19, #4]
	ldur	w11, [x20, #-8]
	cmp	w10, w8
	b.ge	LBB7_29
; %bb.27:                               ;   in Loop: Header=BB7_2 Depth=2
	cmp	w11, w10
	b.ge	LBB7_35
; %bb.28:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w11, [x19, #4]
	b	LBB7_37
LBB7_29:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	w11, w10
	b.ge	LBB7_38
; %bb.30:                               ;   in Loop: Header=BB7_2 Depth=2
	stur	w11, [x9, #-4]
	stur	w10, [x20, #-8]
	ldur	w8, [x9, #-4]
	ldr	w10, [x19, #4]
	cmp	w8, w10
	b.ge	LBB7_38
; %bb.31:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w8, [x19, #4]
	stur	w10, [x9, #-4]
	b	LBB7_38
LBB7_32:                                ;   in Loop: Header=BB7_2 Depth=2
	str	w11, [x9]
	str	w8, [x19]
	ldur	w9, [x20, #-4]
	cmp	w9, w8
	b.ge	LBB7_58
; %bb.33:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w9, [x19]
LBB7_34:                                ;   in Loop: Header=BB7_2 Depth=2
	stur	w8, [x20, #-4]
	b	LBB7_58
LBB7_35:                                ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x19, #4]
	stur	w8, [x9, #-4]
	ldur	w10, [x20, #-8]
	cmp	w10, w8
	b.ge	LBB7_38
; %bb.36:                               ;   in Loop: Header=BB7_2 Depth=2
	stur	w10, [x9, #-4]
LBB7_37:                                ;   in Loop: Header=BB7_2 Depth=2
	stur	w8, [x20, #-8]
LBB7_38:                                ;   in Loop: Header=BB7_2 Depth=2
	ldr	w10, [x9, #4]
	ldr	w8, [x19, #8]
	ldur	w11, [x20, #-12]
	cmp	w10, w8
	b.ge	LBB7_41
; %bb.39:                               ;   in Loop: Header=BB7_2 Depth=2
	cmp	w11, w10
	b.ge	LBB7_44
; %bb.40:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w11, [x19, #8]
	b	LBB7_46
LBB7_41:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	w11, w10
	b.ge	LBB7_47
; %bb.42:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w11, [x9, #4]
	stur	w10, [x20, #-12]
	ldr	w8, [x9, #4]
	ldr	w10, [x19, #8]
	cmp	w8, w10
	b.ge	LBB7_47
; %bb.43:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w8, [x19, #8]
	str	w10, [x9, #4]
	b	LBB7_47
LBB7_44:                                ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x19, #8]
	str	w8, [x9, #4]
	ldur	w10, [x20, #-12]
	cmp	w10, w8
	b.ge	LBB7_47
; %bb.45:                               ;   in Loop: Header=BB7_2 Depth=2
	str	w10, [x9, #4]
LBB7_46:                                ;   in Loop: Header=BB7_2 Depth=2
	stur	w8, [x20, #-12]
LBB7_47:                                ;   in Loop: Header=BB7_2 Depth=2
	ldp	w8, w11, [x9, #-4]
	ldr	w10, [x9, #4]
	cmp	w11, w8
	b.ge	LBB7_50
; %bb.48:                               ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_54
; %bb.49:                               ;   in Loop: Header=BB7_2 Depth=2
	stur	w10, [x9, #-4]
	str	w8, [x9, #4]
	b	LBB7_53
LBB7_50:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	w10, w11
	b.ge	LBB7_53
; %bb.51:                               ;   in Loop: Header=BB7_2 Depth=2
	stp	w10, w11, [x9]
	cmp	w10, w8
	b.ge	LBB7_56
; %bb.52:                               ;   in Loop: Header=BB7_2 Depth=2
	stp	w10, w8, [x9, #-4]
	b	LBB7_57
LBB7_53:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	x8, x11
	b	LBB7_57
LBB7_54:                                ;   in Loop: Header=BB7_2 Depth=2
	stp	w11, w8, [x9, #-4]
	cmp	w10, w8
	b.ge	LBB7_57
; %bb.55:                               ;   in Loop: Header=BB7_2 Depth=2
	stp	w10, w8, [x9]
LBB7_56:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	x8, x10
LBB7_57:                                ;   in Loop: Header=BB7_2 Depth=2
	ldr	w10, [x19]
	str	w8, [x19]
	str	w10, [x9]
LBB7_58:                                ;   in Loop: Header=BB7_2 Depth=2
	sub	x21, x21, #1
	ldr	w8, [x19]
	tbnz	w22, #0, LBB7_60
; %bb.59:                               ;   in Loop: Header=BB7_2 Depth=2
	ldur	w9, [x19, #-4]
	cmp	w9, w8
	b.ge	LBB7_80
LBB7_60:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	x12, #0                         ; =0x0
LBB7_61:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	add	x9, x19, x12
	ldr	w11, [x9, #4]
	add	x12, x12, #4
	cmp	w11, w8
	b.lt	LBB7_61
; %bb.62:                               ;   in Loop: Header=BB7_2 Depth=2
	add	x9, x19, x12
	mov	x10, x20
	cmp	x12, #4
	b.eq	LBB7_64
LBB7_63:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	ldr	w12, [x10, #-4]!
	cmp	w12, w8
	b.ge	LBB7_63
	b	LBB7_67
LBB7_64:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	x10, x20
LBB7_65:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	cmp	x9, x10
	b.hs	LBB7_67
; %bb.66:                               ;   in Loop: Header=BB7_65 Depth=3
	ldr	w12, [x10, #-4]!
	cmp	w12, w8
	b.ge	LBB7_65
LBB7_67:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	x9, x10
	b.hs	LBB7_74
; %bb.68:                               ;   in Loop: Header=BB7_2 Depth=2
	ldr	w14, [x10]
	mov	x12, x9
	mov	x13, x10
LBB7_69:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Loop Header: Depth=3
                                        ;         Child Loop BB7_70 Depth 4
                                        ;         Child Loop BB7_71 Depth 4
	str	w14, [x12]
	str	w11, [x13]
LBB7_70:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ;       Parent Loop BB7_69 Depth=3
                                        ; =>      This Inner Loop Header: Depth=4
	ldr	w11, [x12, #4]!
	cmp	w11, w8
	b.lt	LBB7_70
LBB7_71:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ;       Parent Loop BB7_69 Depth=3
                                        ; =>      This Inner Loop Header: Depth=4
	ldr	w14, [x13, #-4]!
	cmp	w14, w8
	b.ge	LBB7_71
; %bb.72:                               ;   in Loop: Header=BB7_69 Depth=3
	cmp	x12, x13
	b.lo	LBB7_69
; %bb.73:                               ;   in Loop: Header=BB7_2 Depth=2
	sub	x24, x12, #4
	cmp	x19, x24
	b.ne	LBB7_75
	b	LBB7_76
LBB7_74:                                ;   in Loop: Header=BB7_2 Depth=2
	sub	x24, x9, #4
	cmp	x19, x24
	b.eq	LBB7_76
LBB7_75:                                ;   in Loop: Header=BB7_2 Depth=2
	ldr	w11, [x24]
	str	w11, [x19]
LBB7_76:                                ;   in Loop: Header=BB7_2 Depth=2
	str	w8, [x24]
	cmp	x9, x10
	b.lo	LBB7_79
; %bb.77:                               ;   in Loop: Header=BB7_2 Depth=2
	mov	x0, x19
	mov	x1, x24
	bl	__ZNSt3__127__insertion_sort_incompleteB9nqe220106INS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiEEbT1_S6_T0_
	mov	x25, x0
	add	x23, x24, #4
	mov	x0, x23
	mov	x1, x20
	bl	__ZNSt3__127__insertion_sort_incompleteB9nqe220106INS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiEEbT1_S6_T0_
	cbnz	w0, LBB7_98
; %bb.78:                               ;   in Loop: Header=BB7_2 Depth=2
	tbnz	w25, #0, LBB7_2
LBB7_79:                                ;   in Loop: Header=BB7_2 Depth=2
	and	w3, w22, #0x1
	mov	x0, x19
	mov	x1, x24
	mov	x2, x21
	bl	__ZNSt3__111__introsortINS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiLb0EEEvT1_S6_T0_NS_15iterator_traitsIS6_E15difference_typeEb
	mov	w22, #0                         ; =0x0
	add	x23, x24, #4
	b	LBB7_2
LBB7_80:                                ;   in Loop: Header=BB7_2 Depth=2
	ldur	w9, [x20, #-4]
	cmp	w8, w9
	b.ge	LBB7_83
; %bb.81:                               ;   in Loop: Header=BB7_2 Depth=2
	mov	x23, x19
LBB7_82:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	ldr	w9, [x23, #4]!
	cmp	w8, w9
	b.ge	LBB7_82
	b	LBB7_86
LBB7_83:                                ;   in Loop: Header=BB7_2 Depth=2
	add	x9, x19, #4
LBB7_84:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	mov	x23, x9
	cmp	x9, x20
	b.hs	LBB7_86
; %bb.85:                               ;   in Loop: Header=BB7_84 Depth=3
	mov	x9, x23
	ldr	w10, [x9], #4
	cmp	w8, w10
	b.ge	LBB7_84
LBB7_86:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	x9, x20
	cmp	x23, x20
	b.hs	LBB7_89
; %bb.87:                               ;   in Loop: Header=BB7_2 Depth=2
	mov	x9, x20
LBB7_88:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Inner Loop Header: Depth=3
	ldr	w10, [x9, #-4]!
	cmp	w8, w10
	b.lt	LBB7_88
LBB7_89:                                ;   in Loop: Header=BB7_2 Depth=2
	cmp	x23, x9
	b.hs	LBB7_95
; %bb.90:                               ;   in Loop: Header=BB7_2 Depth=2
	ldr	w10, [x23]
	ldr	w11, [x9]
LBB7_91:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ; =>    This Loop Header: Depth=3
                                        ;         Child Loop BB7_92 Depth 4
                                        ;         Child Loop BB7_93 Depth 4
	str	w11, [x23]
	str	w10, [x9]
LBB7_92:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ;       Parent Loop BB7_91 Depth=3
                                        ; =>      This Inner Loop Header: Depth=4
	ldr	w10, [x23, #4]!
	cmp	w8, w10
	b.ge	LBB7_92
LBB7_93:                                ;   Parent Loop BB7_1 Depth=1
                                        ;     Parent Loop BB7_2 Depth=2
                                        ;       Parent Loop BB7_91 Depth=3
                                        ; =>      This Inner Loop Header: Depth=4
	ldr	w11, [x9, #-4]!
	cmp	w8, w11
	b.lt	LBB7_93
; %bb.94:                               ;   in Loop: Header=BB7_91 Depth=3
	cmp	x23, x9
	b.lo	LBB7_91
LBB7_95:                                ;   in Loop: Header=BB7_2 Depth=2
	sub	x9, x23, #4
	cmp	x19, x9
	b.eq	LBB7_97
; %bb.96:                               ;   in Loop: Header=BB7_2 Depth=2
	ldr	w10, [x9]
	str	w10, [x19]
LBB7_97:                                ;   in Loop: Header=BB7_2 Depth=2
	mov	w22, #0                         ; =0x0
	str	w8, [x9]
	b	LBB7_2
LBB7_98:                                ;   in Loop: Header=BB7_1 Depth=1
	mov	x20, x24
	tbz	w25, #0, LBB7_1
	b	LBB7_187
LBB7_99:
	ldp	w9, w8, [x19]
	ldr	w11, [x19, #8]
	cmp	w8, w9
	b.ge	LBB7_146
; %bb.100:
	cmp	w11, w8
	b.ge	LBB7_160
; %bb.101:
	str	w11, [x19]
	str	w9, [x19, #8]
	mov	x10, x11
	mov	x12, x8
	b	LBB7_162
LBB7_102:
	ldur	w8, [x20, #-4]
	ldr	w9, [x19]
	cmp	w8, w9
	b.ge	LBB7_187
; %bb.103:
	str	w8, [x19]
	stur	w9, [x20, #-4]
	b	LBB7_187
LBB7_104:
	ldp	w8, w9, [x19]
	ldur	w10, [x20, #-4]
	cmp	w9, w8
	b.ge	LBB7_149
; %bb.105:
	cmp	w10, w9
	b.ge	LBB7_164
; %bb.106:
	str	w10, [x19]
	stur	w8, [x20, #-4]
	b	LBB7_187
LBB7_107:
	ldp	w9, w8, [x19]
	ldr	w10, [x19, #8]
	cmp	w8, w9
	b.ge	LBB7_151
; %bb.108:
	cmp	w10, w8
	b.ge	LBB7_166
; %bb.109:
	str	w10, [x19]
	b	LBB7_168
LBB7_110:
	cmp	x19, x20
	add	x10, x19, #4
	ccmp	x10, x20, #4, ne
	cset	w8, eq
	tbz	w22, #0, LBB7_154
; %bb.111:
	tbnz	w8, #0, LBB7_187
; %bb.112:
	mov	x8, #0                          ; =0x0
	mov	x11, x19
	b	LBB7_116
LBB7_113:                               ;   in Loop: Header=BB7_116 Depth=1
	mov	x13, x19
LBB7_114:                               ;   in Loop: Header=BB7_116 Depth=1
	str	w10, [x13]
LBB7_115:                               ;   in Loop: Header=BB7_116 Depth=1
	add	x10, x9, #4
	add	x8, x8, #4
	mov	x11, x9
	cmp	x10, x20
	b.eq	LBB7_187
LBB7_116:                               ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB7_118 Depth 2
	mov	x9, x10
	ldp	w12, w10, [x11]
	cmp	w10, w12
	b.ge	LBB7_115
; %bb.117:                              ;   in Loop: Header=BB7_116 Depth=1
	str	w12, [x11, #4]
	mov	x12, x8
	mov	x13, x19
	cmp	x11, x19
	b.eq	LBB7_114
LBB7_118:                               ;   Parent Loop BB7_116 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	add	x13, x19, x12
	ldur	w11, [x13, #-4]
	cmp	w10, w11
	b.ge	LBB7_114
; %bb.119:                              ;   in Loop: Header=BB7_118 Depth=2
	str	w11, [x13]
	subs	x12, x12, #4
	b.ne	LBB7_118
	b	LBB7_113
LBB7_120:
	cmp	x19, x20
	b.eq	LBB7_187
; %bb.121:
	ubfx	x11, x10, #2, #1
	add	x10, x19, #8
	add	x11, x8, x11
	sub	x11, x11, #3
	lsr	x11, x11, #1
	mov	x12, x11
	b	LBB7_124
LBB7_122:                               ;   in Loop: Header=BB7_124 Depth=1
	str	w13, [x19, x15, lsl #2]
LBB7_123:                               ;   in Loop: Header=BB7_124 Depth=1
	cmp	x12, #0
	sub	x12, x12, #1
	b.le	LBB7_129
LBB7_124:                               ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB7_127 Depth 2
	cmp	x11, x12
	b.lo	LBB7_123
; %bb.125:                              ;   in Loop: Header=BB7_124 Depth=1
	mov	w13, #1                         ; =0x1
	bfi	x13, x12, #1, #62
	ldr	w13, [x19, x13, lsl #2]
	lsl	x14, x12, #1
	lsl	x15, x12, #3
	ldr	w15, [x10, x15]
	cmp	w13, w15
	add	x13, x14, #2
	csinc	x14, x13, x14, lt
	ldr	w16, [x19, x14, lsl #2]
	ldr	w13, [x19, x12, lsl #2]
	cmp	w16, w13
	b.lt	LBB7_123
; %bb.126:                              ;   in Loop: Header=BB7_124 Depth=1
	mov	x15, x12
LBB7_127:                               ;   Parent Loop BB7_124 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	str	w16, [x19, x15, lsl #2]
	mov	x15, x14
	cmp	x11, x14
	b.lt	LBB7_122
; %bb.128:                              ;   in Loop: Header=BB7_127 Depth=2
	lsl	x14, x15, #1
	mov	w16, #1                         ; =0x1
	bfi	x16, x15, #1, #62
	ldr	w16, [x19, x16, lsl #2]
	lsl	x17, x15, #3
	ldr	w17, [x10, x17]
	cmp	w16, w17
	add	x16, x14, #2
	csinc	x14, x16, x14, lt
	ldr	w16, [x19, x14, lsl #2]
	cmp	w16, w13
	b.ge	LBB7_127
	b	LBB7_122
LBB7_129:
	lsr	x9, x9, #1
	add	x12, x19, x9, lsl #2
	ldr	w11, [x12]
	mov	x13, x20
	ldr	w10, [x13, #-4]!
	cmp	w11, w10
	b.ge	LBB7_135
LBB7_130:                               ; =>This Inner Loop Header: Depth=1
	mov	x14, x12
	str	w11, [x13]
	cbz	x9, LBB7_132
; %bb.131:                              ;   in Loop: Header=BB7_130 Depth=1
	sub	x9, x9, #1
	lsr	x9, x9, #1
	add	x12, x19, x9, lsl #2
	ldr	w11, [x12]
	mov	x13, x14
	cmp	w11, w10
	b.lt	LBB7_130
LBB7_132:
	str	w10, [x14]
	b	LBB7_135
LBB7_133:                               ;   in Loop: Header=BB7_135 Depth=1
	str	w10, [x9]
LBB7_134:                               ;   in Loop: Header=BB7_135 Depth=1
	cmp	x8, #2
	sub	x8, x8, #1
	b.le	LBB7_187
LBB7_135:                               ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB7_138 Depth 2
                                        ;     Child Loop BB7_143 Depth 2
	mov	x13, #0                         ; =0x0
	ldr	w10, [x19]
	sub	x9, x8, #2
	lsr	x11, x9, #1
	mov	x12, x19
	b	LBB7_138
LBB7_136:                               ;   in Loop: Header=BB7_138 Depth=2
	ldr	w17, [x16, #8]!
	cmp	w14, w17
	csel	w14, w14, w17, gt
	csel	x9, x16, x9, lt
	csel	x13, x13, x15, lt
LBB7_137:                               ;   in Loop: Header=BB7_138 Depth=2
	str	w14, [x12]
	mov	x12, x9
	cmp	x13, x11
	b.gt	LBB7_140
LBB7_138:                               ;   Parent Loop BB7_135 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	add	x16, x12, x13, lsl #2
	mov	x9, x16
	ldr	w14, [x9, #4]!
	lsl	x17, x13, #1
	mov	w15, #1                         ; =0x1
	bfi	x15, x13, #1, #63
	add	x13, x17, #2
	cmp	x13, x8
	b.lt	LBB7_136
; %bb.139:                              ;   in Loop: Header=BB7_138 Depth=2
	mov	x13, x15
	b	LBB7_137
LBB7_140:                               ;   in Loop: Header=BB7_135 Depth=1
	sub	x20, x20, #4
	cmp	x9, x20
	b.eq	LBB7_133
; %bb.141:                              ;   in Loop: Header=BB7_135 Depth=1
	ldr	w11, [x20]
	str	w11, [x9]
	str	w10, [x20]
	sub	x10, x9, x19
	add	x10, x10, #4
	asr	x10, x10, #2
	subs	x10, x10, #2
	b.lt	LBB7_134
; %bb.142:                              ;   in Loop: Header=BB7_135 Depth=1
	lsr	x10, x10, #1
	add	x13, x19, x10, lsl #2
	ldr	w12, [x13]
	ldr	w11, [x9]
	cmp	w12, w11
	b.ge	LBB7_134
LBB7_143:                               ;   Parent Loop BB7_135 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	mov	x14, x13
	str	w12, [x9]
	cbz	x10, LBB7_145
; %bb.144:                              ;   in Loop: Header=BB7_143 Depth=2
	sub	x9, x10, #1
	lsr	x10, x9, #1
	add	x13, x19, x10, lsl #2
	ldr	w12, [x13]
	mov	x9, x14
	cmp	w12, w11
	b.lt	LBB7_143
LBB7_145:                               ;   in Loop: Header=BB7_135 Depth=1
	str	w11, [x14]
	b	LBB7_134
LBB7_146:
	cmp	w11, w8
	b.ge	LBB7_163
; %bb.147:
	stp	w11, w8, [x19, #4]
	cmp	w11, w9
	b.ge	LBB7_172
; %bb.148:
	stp	w11, w9, [x19]
	mov	x10, x11
	mov	x12, x9
	b	LBB7_175
LBB7_149:
	cmp	w10, w9
	b.ge	LBB7_187
; %bb.150:
	str	w10, [x19, #4]
	stur	w9, [x20, #-4]
	ldr	w8, [x19, #4]
	b	LBB7_185
LBB7_151:
	cmp	w10, w8
	b.ge	LBB7_169
; %bb.152:
	stp	w10, w8, [x19, #4]
	cmp	w10, w9
	b.ge	LBB7_170
; %bb.153:
	stp	w10, w9, [x19]
	b	LBB7_170
LBB7_154:
	tbz	w8, #0, LBB7_156
	b	LBB7_187
LBB7_155:                               ;   in Loop: Header=BB7_156 Depth=1
	add	x10, x19, #4
	cmp	x10, x20
	b.eq	LBB7_187
LBB7_156:                               ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB7_158 Depth 2
	ldp	w9, w8, [x19]
	mov	x19, x10
	cmp	w8, w9
	b.ge	LBB7_155
; %bb.157:                              ;   in Loop: Header=BB7_156 Depth=1
	mov	x10, x19
LBB7_158:                               ;   Parent Loop BB7_156 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	str	w9, [x10]
	ldur	w9, [x10, #-8]
	sub	x10, x10, #4
	cmp	w8, w9
	b.lt	LBB7_158
; %bb.159:                              ;   in Loop: Header=BB7_156 Depth=1
	str	w8, [x10]
	b	LBB7_155
LBB7_160:
	stp	w8, w9, [x19]
	cmp	w11, w9
	b.ge	LBB7_173
; %bb.161:
	stp	w11, w9, [x19, #4]
	mov	x10, x8
	mov	x12, x11
LBB7_162:
	mov	x8, x9
	b	LBB7_175
LBB7_163:
	mov	x10, x9
	mov	x12, x8
	b	LBB7_174
LBB7_164:
	stp	w9, w8, [x19]
	ldur	w9, [x20, #-4]
	cmp	w9, w8
	b.ge	LBB7_187
; %bb.165:
	str	w9, [x19, #4]
	stur	w8, [x20, #-4]
	b	LBB7_187
LBB7_166:
	stp	w8, w9, [x19]
	cmp	w10, w9
	b.ge	LBB7_169
; %bb.167:
	str	w10, [x19, #4]
LBB7_168:
	str	w9, [x19, #8]
	mov	x8, x9
	b	LBB7_170
LBB7_169:
	mov	x8, x10
LBB7_170:
	ldur	w9, [x20, #-4]
	cmp	w9, w8
	b.ge	LBB7_187
; %bb.171:
	str	w9, [x19, #8]
	stur	w8, [x20, #-4]
	ldr	w8, [x19, #8]
	b	LBB7_183
LBB7_172:
	mov	x10, x9
	mov	x12, x11
	b	LBB7_175
LBB7_173:
	mov	x10, x8
	mov	x12, x9
LBB7_174:
	mov	x8, x11
LBB7_175:
	ldr	w9, [x19, #12]
	cmp	w9, w8
	b.ge	LBB7_179
; %bb.176:
	stp	w9, w8, [x19, #8]
	cmp	w9, w12
	b.ge	LBB7_180
; %bb.177:
	stp	w9, w12, [x19, #4]
	cmp	w9, w10
	b.ge	LBB7_180
; %bb.178:
	stp	w9, w10, [x19]
	b	LBB7_180
LBB7_179:
	mov	x8, x9
LBB7_180:
	ldur	w9, [x20, #-4]
	cmp	w9, w8
	b.ge	LBB7_187
; %bb.181:
	str	w9, [x19, #12]
	stur	w8, [x20, #-4]
	ldp	w9, w8, [x19, #8]
	cmp	w8, w9
	b.ge	LBB7_187
; %bb.182:
	stp	w8, w9, [x19, #8]
LBB7_183:
	ldr	w9, [x19, #4]
	cmp	w8, w9
	b.ge	LBB7_187
; %bb.184:
	stp	w8, w9, [x19, #4]
LBB7_185:
	ldr	w9, [x19]
	cmp	w8, w9
	b.ge	LBB7_187
; %bb.186:
	stp	w8, w9, [x19]
LBB7_187:
	ldp	x29, x30, [sp, #64]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #48]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #32]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #16]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp], #80             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.p2align	2                               ; -- Begin function _ZNSt3__127__insertion_sort_incompleteB9nqe220106INS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiEEbT1_S6_T0_
__ZNSt3__127__insertion_sort_incompleteB9nqe220106INS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiEEbT1_S6_T0_: ; @"_ZNSt3__127__insertion_sort_incompleteB9nqe220106INS_17_ClassicAlgPolicyERZZ4mainENK3$_2clEvEUliiE_PiEEbT1_S6_T0_"
	.cfi_startproc
; %bb.0:
	sub	x8, x1, x0
	asr	x8, x8, #2
	cmp	x8, #2
	b.gt	LBB8_3
; %bb.1:
	b.hs	LBB8_9
LBB8_2:
	mov	w0, #1                          ; =0x1
	ret
LBB8_3:
	cmp	x8, #3
	b.eq	LBB8_12
; %bb.4:
	cmp	x8, #4
	b.eq	LBB8_18
; %bb.5:
	cmp	x8, #5
	b.ne	LBB8_15
; %bb.6:
	ldp	w9, w8, [x0]
	ldr	w11, [x0, #8]
	cmp	w8, w9
	b.ge	LBB8_26
; %bb.7:
	cmp	w11, w8
	b.ge	LBB8_48
; %bb.8:
	str	w11, [x0]
	str	w9, [x0, #8]
	mov	x10, x11
	mov	x12, x8
	b	LBB8_50
LBB8_9:
	cmp	x8, #2
	b.ne	LBB8_15
; %bb.10:
	ldur	w8, [x1, #-4]
	ldr	w9, [x0]
	cmp	w8, w9
	b.ge	LBB8_2
; %bb.11:
	str	w8, [x0]
	stur	w9, [x1, #-4]
	mov	w0, #1                          ; =0x1
	ret
LBB8_12:
	ldp	w8, w9, [x0]
	ldur	w10, [x1, #-4]
	cmp	w9, w8
	b.ge	LBB8_21
; %bb.13:
	cmp	w10, w9
	b.ge	LBB8_32
; %bb.14:
	str	w10, [x0]
	b	LBB8_34
LBB8_15:
	mov	x11, x0
	ldr	w9, [x11, #8]!
	ldp	w8, w10, [x0]
	cmp	w10, w8
	b.ge	LBB8_23
; %bb.16:
	cmp	w9, w10
	b.ge	LBB8_35
; %bb.17:
	str	w9, [x0]
	b	LBB8_37
LBB8_18:
	ldp	w9, w8, [x0]
	ldr	w10, [x0, #8]
	cmp	w8, w9
	b.ge	LBB8_29
; %bb.19:
	cmp	w10, w8
	b.ge	LBB8_52
; %bb.20:
	str	w10, [x0]
	b	LBB8_54
LBB8_21:
	cmp	w10, w9
	b.ge	LBB8_2
; %bb.22:
	str	w10, [x0, #4]
	stur	w9, [x1, #-4]
	ldr	w8, [x0, #4]
	b	LBB8_72
LBB8_23:
	cmp	w9, w10
	b.ge	LBB8_38
; %bb.24:
	stp	w9, w10, [x0, #4]
	cmp	w9, w8
	b.ge	LBB8_38
; %bb.25:
	stp	w9, w8, [x0]
	b	LBB8_38
LBB8_26:
	cmp	w11, w8
	b.ge	LBB8_51
; %bb.27:
	stp	w11, w8, [x0, #4]
	cmp	w11, w9
	b.ge	LBB8_59
; %bb.28:
	stp	w11, w9, [x0]
	mov	x10, x11
	mov	x12, x9
	b	LBB8_62
LBB8_29:
	cmp	w10, w8
	b.ge	LBB8_55
; %bb.30:
	stp	w10, w8, [x0, #4]
	cmp	w10, w9
	b.ge	LBB8_56
; %bb.31:
	stp	w10, w9, [x0]
	b	LBB8_56
LBB8_32:
	stp	w9, w8, [x0]
	ldur	w9, [x1, #-4]
	cmp	w9, w8
	b.ge	LBB8_2
; %bb.33:
	str	w9, [x0, #4]
LBB8_34:
	stur	w8, [x1, #-4]
	mov	w0, #1                          ; =0x1
	ret
LBB8_35:
	stp	w10, w8, [x0]
	cmp	w9, w8
	b.ge	LBB8_38
; %bb.36:
	str	w9, [x0, #4]
LBB8_37:
	str	w8, [x0, #8]
LBB8_38:
	add	x8, x0, #12
	cmp	x8, x1
	b.eq	LBB8_2
; %bb.39:
	mov	x9, #0                          ; =0x0
	mov	w10, #0                         ; =0x0
	b	LBB8_43
LBB8_40:                                ;   in Loop: Header=BB8_43 Depth=1
	add	x11, x13, #8
LBB8_41:                                ;   in Loop: Header=BB8_43 Depth=1
	str	w12, [x11]
	add	w10, w10, #1
	cmp	w10, #8
	b.eq	LBB8_58
LBB8_42:                                ;   in Loop: Header=BB8_43 Depth=1
	mov	x11, x8
	add	x8, x8, #4
	add	x9, x9, #4
	cmp	x8, x1
	b.eq	LBB8_2
LBB8_43:                                ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB8_45 Depth 2
	ldr	w12, [x8]
	ldr	w11, [x11]
	cmp	w12, w11
	b.ge	LBB8_42
; %bb.44:                               ;   in Loop: Header=BB8_43 Depth=1
	str	w11, [x8]
	mov	x11, x9
LBB8_45:                                ;   Parent Loop BB8_43 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	add	x13, x0, x11
	ldr	w14, [x13, #4]
	cmp	w12, w14
	b.ge	LBB8_40
; %bb.46:                               ;   in Loop: Header=BB8_45 Depth=2
	str	w14, [x13, #8]
	sub	x11, x11, #4
	cmn	x11, #8
	b.ne	LBB8_45
; %bb.47:                               ;   in Loop: Header=BB8_43 Depth=1
	mov	x11, x0
	b	LBB8_41
LBB8_48:
	stp	w8, w9, [x0]
	cmp	w11, w9
	b.ge	LBB8_60
; %bb.49:
	stp	w11, w9, [x0, #4]
	mov	x10, x8
	mov	x12, x11
LBB8_50:
	mov	x8, x9
	b	LBB8_62
LBB8_51:
	mov	x10, x9
	mov	x12, x8
	b	LBB8_61
LBB8_52:
	stp	w8, w9, [x0]
	cmp	w10, w9
	b.ge	LBB8_55
; %bb.53:
	str	w10, [x0, #4]
LBB8_54:
	str	w9, [x0, #8]
	mov	x8, x9
	b	LBB8_56
LBB8_55:
	mov	x8, x10
LBB8_56:
	ldur	w9, [x1, #-4]
	cmp	w9, w8
	b.ge	LBB8_2
; %bb.57:
	str	w9, [x0, #8]
	stur	w8, [x1, #-4]
	ldr	w8, [x0, #8]
	b	LBB8_70
LBB8_58:
	add	x8, x8, #4
	cmp	x8, x1
	cset	w0, eq
	ret
LBB8_59:
	mov	x10, x9
	mov	x12, x11
	b	LBB8_62
LBB8_60:
	mov	x10, x8
	mov	x12, x9
LBB8_61:
	mov	x8, x11
LBB8_62:
	ldr	w9, [x0, #12]
	cmp	w9, w8
	b.ge	LBB8_66
; %bb.63:
	stp	w9, w8, [x0, #8]
	cmp	w9, w12
	b.ge	LBB8_67
; %bb.64:
	stp	w9, w12, [x0, #4]
	cmp	w9, w10
	b.ge	LBB8_67
; %bb.65:
	stp	w9, w10, [x0]
	b	LBB8_67
LBB8_66:
	mov	x8, x9
LBB8_67:
	ldur	w9, [x1, #-4]
	cmp	w9, w8
	b.ge	LBB8_2
; %bb.68:
	str	w9, [x0, #12]
	stur	w8, [x1, #-4]
	ldp	w9, w8, [x0, #8]
	cmp	w8, w9
	b.ge	LBB8_2
; %bb.69:
	stp	w8, w9, [x0, #8]
LBB8_70:
	ldr	w9, [x0, #4]
	cmp	w8, w9
	b.ge	LBB8_2
; %bb.71:
	stp	w8, w9, [x0, #4]
LBB8_72:
	ldr	w9, [x0]
	cmp	w8, w9
	b.ge	LBB8_2
; %bb.73:
	stp	w8, w9, [x0]
	mov	w0, #1                          ; =0x1
	ret
	.cfi_endproc
                                        ; -- End function
	.p2align	2                               ; -- Begin function _ZL7cmp_intPKvS0_
__ZL7cmp_intPKvS0_:                     ; @_ZL7cmp_intPKvS0_
	.cfi_startproc
; %bb.0:
	ldr	w8, [x0]
	ldr	w9, [x1]
	cmp	w8, w9
	cset	w8, gt
	csinv	w0, w8, wzr, ge
	ret
	.cfi_endproc
                                        ; -- End function
	.private_extern	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m ; -- Begin function _ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
	.globl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
	.weak_def_can_be_hidden	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
	.p2align	2
__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m: ; @_ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Lfunc_begin2:
	.cfi_startproc
	.cfi_personality 155, ___gxx_personality_v0
	.cfi_lsda 16, Lexception2
; %bb.0:
	sub	sp, sp, #112
	stp	x26, x25, [sp, #32]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #48]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #64]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #80]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #96]             ; 16-byte Folded Spill
	add	x29, sp, #96
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	mov	x21, x2
	mov	x20, x1
	mov	x19, x0
Ltmp54:
	add	x0, sp, #8
	mov	x1, x19
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryC1ERS3_
Ltmp55:
; %bb.1:
	ldrb	w8, [sp, #8]
	cmp	w8, #1
	b.ne	LBB10_10
; %bb.2:
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
	add	x4, x19, x8
	ldr	x22, [x4, #40]
	ldr	w24, [x4, #8]
	ldr	w23, [x4, #144]
	cmn	w23, #1
	b.ne	LBB10_7
; %bb.3:
Ltmp57:
	add	x8, sp, #24
	mov	x25, x4
	mov	x0, x4
	bl	__ZNKSt3__18ios_base6getlocEv
Ltmp58:
; %bb.4:
Ltmp59:
Lloh36:
	adrp	x1, __ZNSt3__15ctypeIcE2idE@GOTPAGE
Lloh37:
	ldr	x1, [x1, __ZNSt3__15ctypeIcE2idE@GOTPAGEOFF]
	add	x0, sp, #24
	bl	__ZNKSt3__16locale9use_facetERNS0_2idE
Ltmp60:
; %bb.5:
	ldr	x8, [x0]
	ldr	x8, [x8, #56]
Ltmp61:
	mov	w1, #32                         ; =0x20
	blr	x8
Ltmp62:
; %bb.6:
	mov	x23, x0
	add	x0, sp, #24
	bl	__ZNSt3__16localeD1Ev
	mov	x4, x25
	str	w23, [x25, #144]
LBB10_7:
	mov	w8, #176                        ; =0xb0
	and	w8, w24, w8
	add	x3, x20, x21
	cmp	w8, #32
	csel	x2, x3, x20, eq
Ltmp64:
	sxtb	w5, w23
	mov	x0, x22
	mov	x1, x20
	bl	__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
Ltmp65:
; %bb.8:
	cbnz	x0, LBB10_10
; %bb.9:
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
	add	x0, x19, x8
	ldr	w8, [x0, #32]
	mov	w9, #5                          ; =0x5
Ltmp67:
	orr	w1, w8, w9
	bl	__ZNSt3__18ios_base5clearEj
Ltmp68:
LBB10_10:
	add	x0, sp, #8
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryD1Ev
LBB10_11:
	mov	x0, x19
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #80]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #64]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #48]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #112
	ret
LBB10_12:
Ltmp69:
	b	LBB10_15
LBB10_13:
Ltmp63:
	mov	x20, x0
	add	x0, sp, #24
	bl	__ZNSt3__16localeD1Ev
	b	LBB10_16
LBB10_14:
Ltmp66:
LBB10_15:
	mov	x20, x0
LBB10_16:
	add	x0, sp, #8
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryD1Ev
	b	LBB10_18
LBB10_17:
Ltmp56:
	mov	x20, x0
LBB10_18:
	mov	x0, x20
	bl	___cxa_begin_catch
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
Ltmp70:
	add	x0, x19, x8
	bl	__ZNSt3__18ios_base33__set_badbit_and_consider_rethrowEv
Ltmp71:
; %bb.19:
	bl	___cxa_end_catch
	b	LBB10_11
LBB10_20:
Ltmp72:
	mov	x19, x0
Ltmp73:
	bl	___cxa_end_catch
Ltmp74:
; %bb.21:
	mov	x0, x19
	bl	__Unwind_Resume
LBB10_22:
Ltmp75:
	bl	___clang_call_terminate
	.loh AdrpLdrGot	Lloh36, Lloh37
Lfunc_end2:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table10:
Lexception2:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	155                             ; @TType Encoding = indirect pcrel sdata4
	.uleb128 Lttbase0-Lttbaseref0
Lttbaseref0:
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end2-Lcst_begin2
Lcst_begin2:
	.uleb128 Ltmp54-Lfunc_begin2            ; >> Call Site 1 <<
	.uleb128 Ltmp55-Ltmp54                  ;   Call between Ltmp54 and Ltmp55
	.uleb128 Ltmp56-Lfunc_begin2            ;     jumps to Ltmp56
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp57-Lfunc_begin2            ; >> Call Site 2 <<
	.uleb128 Ltmp58-Ltmp57                  ;   Call between Ltmp57 and Ltmp58
	.uleb128 Ltmp66-Lfunc_begin2            ;     jumps to Ltmp66
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp59-Lfunc_begin2            ; >> Call Site 3 <<
	.uleb128 Ltmp62-Ltmp59                  ;   Call between Ltmp59 and Ltmp62
	.uleb128 Ltmp63-Lfunc_begin2            ;     jumps to Ltmp63
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp64-Lfunc_begin2            ; >> Call Site 4 <<
	.uleb128 Ltmp65-Ltmp64                  ;   Call between Ltmp64 and Ltmp65
	.uleb128 Ltmp66-Lfunc_begin2            ;     jumps to Ltmp66
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp67-Lfunc_begin2            ; >> Call Site 5 <<
	.uleb128 Ltmp68-Ltmp67                  ;   Call between Ltmp67 and Ltmp68
	.uleb128 Ltmp69-Lfunc_begin2            ;     jumps to Ltmp69
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp68-Lfunc_begin2            ; >> Call Site 6 <<
	.uleb128 Ltmp70-Ltmp68                  ;   Call between Ltmp68 and Ltmp70
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp70-Lfunc_begin2            ; >> Call Site 7 <<
	.uleb128 Ltmp71-Ltmp70                  ;   Call between Ltmp70 and Ltmp71
	.uleb128 Ltmp72-Lfunc_begin2            ;     jumps to Ltmp72
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp71-Lfunc_begin2            ; >> Call Site 8 <<
	.uleb128 Ltmp73-Ltmp71                  ;   Call between Ltmp71 and Ltmp73
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp73-Lfunc_begin2            ; >> Call Site 9 <<
	.uleb128 Ltmp74-Ltmp73                  ;   Call between Ltmp73 and Ltmp74
	.uleb128 Ltmp75-Lfunc_begin2            ;     jumps to Ltmp75
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp74-Lfunc_begin2            ; >> Call Site 10 <<
	.uleb128 Lfunc_end2-Ltmp74              ;   Call between Ltmp74 and Lfunc_end2
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
Lcst_end2:
	.byte	1                               ; >> Action Record 1 <<
                                        ;   Catch TypeInfo 1
	.byte	0                               ;   No further actions
	.p2align	2, 0x0
                                        ; >> Catch TypeInfos <<
	.long	0                               ; TypeInfo 1
Lttbase0:
	.p2align	2, 0x0
                                        ; -- End function
	.section	__TEXT,__text,regular,pure_instructions
	.private_extern	__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_ ; -- Begin function _ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
	.globl	__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
	.weak_def_can_be_hidden	__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
	.p2align	2
__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_: ; @_ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
Lfunc_begin3:
	.cfi_startproc
	.cfi_personality 155, ___gxx_personality_v0
	.cfi_lsda 16, Lexception3
; %bb.0:
	sub	sp, sp, #112
	stp	x26, x25, [sp, #32]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #48]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #64]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #80]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #96]             ; 16-byte Folded Spill
	add	x29, sp, #96
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	mov	x19, x0
	cbz	x0, LBB11_16
; %bb.1:
	mov	x23, x5
	mov	x20, x4
	mov	x22, x3
	mov	x21, x2
	mov	x24, x1
	ldr	x26, [x4, #24]
	sub	x25, x2, x1
	cmp	x25, #1
	b.lt	LBB11_3
; %bb.2:
	ldr	x8, [x19]
	ldr	x8, [x8, #96]
	mov	x0, x19
	mov	x1, x24
	mov	x2, x25
	blr	x8
	cmp	x0, x25
	b.ne	LBB11_15
LBB11_3:
	sub	x8, x22, x24
	cmp	x26, x8
	b.le	LBB11_12
; %bb.4:
	mov	x9, #-9                         ; =0xfffffffffffffff7
	movk	x9, #32767, lsl #48
	sub	x24, x26, x8
	cmp	x24, x9
	b.hs	LBB11_17
; %bb.5:
	cmp	x24, #23
	b.hs	LBB11_7
; %bb.6:
	strb	w24, [sp, #31]
	add	x25, sp, #8
	b	LBB11_8
LBB11_7:
	and	x8, x24, #0x7ffffffffffffff8
	add	x8, x8, #8
	mov	w9, #25                         ; =0x19
	cmp	x8, #24
	csel	x26, x9, x8, eq
	mov	x0, x26
	bl	__Znwm
	mov	x25, x0
	orr	x8, x26, #0x8000000000000000
	stp	x0, x24, [sp, #8]
	str	x8, [sp, #24]
LBB11_8:
	mov	x0, x25
	mov	x1, x23
	mov	x2, x24
	bl	_memset
	strb	wzr, [x25, x24]
	ldrsb	w8, [sp, #31]
	ldr	x9, [sp, #8]
	cmp	w8, #0
	add	x8, sp, #8
	csel	x1, x9, x8, lt
	ldr	x8, [x19]
	ldr	x8, [x8, #96]
Ltmp76:
	mov	x0, x19
	mov	x2, x24
	blr	x8
Ltmp77:
; %bb.9:
	ldrsb	w8, [sp, #31]
	tbnz	w8, #31, LBB11_11
; %bb.10:
	cmp	x0, x24
	b.ne	LBB11_15
	b	LBB11_12
LBB11_11:
	ldr	x8, [sp, #8]
	mov	x23, x0
	mov	x0, x8
	bl	__ZdlPv
	mov	x0, x23
	cmp	x0, x24
	b.ne	LBB11_15
LBB11_12:
	sub	x22, x22, x21
	cmp	x22, #1
	b.lt	LBB11_14
; %bb.13:
	ldr	x8, [x19]
	ldr	x8, [x8, #96]
	mov	x0, x19
	mov	x1, x21
	mov	x2, x22
	blr	x8
	cmp	x0, x22
	b.ne	LBB11_15
LBB11_14:
	str	xzr, [x20, #24]
	b	LBB11_16
LBB11_15:
	mov	x19, #0                         ; =0x0
LBB11_16:
	mov	x0, x19
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #80]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #64]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #48]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #112
	ret
LBB11_17:
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
LBB11_18:
Ltmp78:
	mov	x19, x0
	ldrsb	w8, [sp, #31]
	tbz	w8, #31, LBB11_20
; %bb.19:
	ldr	x0, [sp, #8]
	bl	__ZdlPv
LBB11_20:
	mov	x0, x19
	bl	__Unwind_Resume
Lfunc_end3:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table11:
Lexception3:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	255                             ; @TType Encoding = omit
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end3-Lcst_begin3
Lcst_begin3:
	.uleb128 Lfunc_begin3-Lfunc_begin3      ; >> Call Site 1 <<
	.uleb128 Ltmp76-Lfunc_begin3            ;   Call between Lfunc_begin3 and Ltmp76
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp76-Lfunc_begin3            ; >> Call Site 2 <<
	.uleb128 Ltmp77-Ltmp76                  ;   Call between Ltmp76 and Ltmp77
	.uleb128 Ltmp78-Lfunc_begin3            ;     jumps to Ltmp78
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp77-Lfunc_begin3            ; >> Call Site 3 <<
	.uleb128 Lfunc_end3-Ltmp77              ;   Call between Ltmp77 and Lfunc_end3
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
Lcst_end3:
	.p2align	2, 0x0
                                        ; -- End function
	.section	__TEXT,__text,regular,pure_instructions
	.private_extern	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev ; -- Begin function _ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
	.globl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
	.weak_def_can_be_hidden	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
	.p2align	2
__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev: ; @_ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
	.cfi_startproc
; %bb.0:
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
Lloh38:
	adrp	x0, l_.str.11@PAGE
Lloh39:
	add	x0, x0, l_.str.11@PAGEOFF
	bl	__ZNSt3__120__throw_length_errorB9nqe220106EPKc
	.loh AdrpAdd	Lloh38, Lloh39
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"QUICK"

l_.str.1:                               ; @.str.1
	.asciz	"sums agree: "

l_.str.2:                               ; @.str.2
	.asciz	"\n"

l_.str.3:                               ; @.str.3
	.asciz	"sort "

l_.str.4:                               ; @.str.4
	.asciz	" ints:  std::sort "

l_.str.5:                               ; @.str.5
	.asciz	" ms,  std::sort + lambda "

l_.str.6:                               ; @.str.6
	.asciz	" ms,  qsort "

l_.str.7:                               ; @.str.7
	.asciz	" ms (qsort/std::sort = "

l_.str.8:                               ; @.str.8
	.asciz	"x)\n"

l_.str.9:                               ; @.str.9
	.asciz	"identical results: "

l_.str.11:                              ; @.str.11
	.asciz	"basic_string"

.subsections_via_symbols
