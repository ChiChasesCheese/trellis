	.build_version macos, 27, 0	sdk_version 27, 0
	.section	__TEXT,__text,regular,pure_instructions
	.globl	__Z8copy_stdPKiS0_Pi            ; -- Begin function _Z8copy_stdPKiS0_Pi
	.p2align	2
__Z8copy_stdPKiS0_Pi:                   ; @_Z8copy_stdPKiS0_Pi
	.cfi_startproc
; %bb.0:
	mov	x9, x2
	mov	x8, x0
	sub	x2, x1, x0
	mov	x0, x9
	mov	x1, x8
	b	_memmove
	.cfi_endproc
                                        ; -- End function
	.globl	__Z11copy_memcpyPKimPi          ; -- Begin function _Z11copy_memcpyPKimPi
	.p2align	2
__Z11copy_memcpyPKimPi:                 ; @_Z11copy_memcpyPKimPi
	.cfi_startproc
; %bb.0:
	mov	x9, x2
	mov	x8, x0
	lsl	x2, x1, #2
	mov	x0, x9
	mov	x1, x8
	b	_memcpy
	.cfi_endproc
                                        ; -- End function
	.globl	__Z9copy_loopPKimPi             ; -- Begin function _Z9copy_loopPKimPi
	.p2align	2
__Z9copy_loopPKimPi:                    ; @_Z9copy_loopPKimPi
	.cfi_startproc
; %bb.0:
	cbz	x1, LBB2_14
; %bb.1:
	mov	x8, #0                          ; =0x0
	cmp	x1, #4
	b.lo	LBB2_12
; %bb.2:
	sub	x9, x2, x0
	cmp	x9, #63
	b.ls	LBB2_12
; %bb.3:
	cmp	x1, #16
	b.hs	LBB2_5
; %bb.4:
	mov	x8, #0                          ; =0x0
	b	LBB2_9
LBB2_5:
	and	x8, x1, #0xfffffffffffffff0
	add	x9, x0, #32
	add	x10, x2, #32
	mov	x11, x8
LBB2_6:                                 ; =>This Inner Loop Header: Depth=1
	ldp	q0, q1, [x9, #-32]
	ldp	q2, q3, [x9], #64
	stp	q0, q1, [x10, #-32]
	stp	q2, q3, [x10], #64
	subs	x11, x11, #16
	b.ne	LBB2_6
; %bb.7:
	cmp	x1, x8
	b.eq	LBB2_14
; %bb.8:
	tst	x1, #0xc
	b.eq	LBB2_12
LBB2_9:
	mov	x10, x8
	and	x8, x1, #0xfffffffffffffffc
	sub	x9, x10, x8
	lsl	x11, x10, #2
	add	x10, x2, x11
	add	x11, x0, x11
LBB2_10:                                ; =>This Inner Loop Header: Depth=1
	ldr	q0, [x11], #16
	str	q0, [x10], #16
	adds	x9, x9, #4
	b.ne	LBB2_10
; %bb.11:
	cmp	x1, x8
	b.eq	LBB2_14
LBB2_12:
	sub	x9, x1, x8
	lsl	x10, x8, #2
	add	x8, x2, x10
	add	x10, x0, x10
LBB2_13:                                ; =>This Inner Loop Header: Depth=1
	ldr	w11, [x10], #4
	str	w11, [x8], #4
	subs	x9, x9, #1
	b.ne	LBB2_13
LBB2_14:
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	__Z12copy_fixed16PKiPi          ; -- Begin function _Z12copy_fixed16PKiPi
	.p2align	2
__Z12copy_fixed16PKiPi:                 ; @_Z12copy_fixed16PKiPi
	.cfi_startproc
; %bb.0:
	ldp	q0, q1, [x0]
	ldp	q2, q3, [x0, #32]
	stp	q2, q3, [x1, #32]
	stp	q0, q1, [x1]
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	__Z12copy_stringsPKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_PS5_ ; -- Begin function _Z12copy_stringsPKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_PS5_
	.p2align	2
__Z12copy_stringsPKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_PS5_: ; @_Z12copy_stringsPKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_PS5_
	.cfi_startproc
; %bb.0:
	cmp	x0, x1
	b.eq	LBB4_10
; %bb.1:
	stp	x22, x21, [sp, #-48]!           ; 16-byte Folded Spill
	stp	x20, x19, [sp, #16]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	mov	x19, x2
	mov	x20, x1
	mov	x21, x0
	b	LBB4_4
LBB4_2:                                 ;   in Loop: Header=BB4_4 Depth=1
	sxtb	w9, w8
	ldp	x10, x11, [x21]
	cmp	w9, #0
	csel	x1, x10, x21, lt
	csel	x2, x11, x8, lt
	mov	x0, x19
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm
LBB4_3:                                 ;   in Loop: Header=BB4_4 Depth=1
	add	x21, x21, #24
	add	x19, x19, #24
	cmp	x21, x20
	b.eq	LBB4_9
LBB4_4:                                 ; =>This Inner Loop Header: Depth=1
	cmp	x21, x19
	b.eq	LBB4_3
; %bb.5:                                ;   in Loop: Header=BB4_4 Depth=1
	ldrsb	w9, [x19, #23]
	ldrb	w8, [x21, #23]
	tbnz	w9, #31, LBB4_2
; %bb.6:                                ;   in Loop: Header=BB4_4 Depth=1
	tbnz	w8, #7, LBB4_8
; %bb.7:                                ;   in Loop: Header=BB4_4 Depth=1
	ldr	q0, [x21]
	ldr	x8, [x21, #16]
	str	x8, [x19, #16]
	str	q0, [x19]
	b	LBB4_3
LBB4_8:                                 ;   in Loop: Header=BB4_4 Depth=1
	ldp	x1, x2, [x21]
	mov	x0, x19
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm
	b	LBB4_3
LBB4_9:
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #16]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp], #48             ; 16-byte Folded Reload
LBB4_10:
	ret
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
	sub	sp, sp, #192
	stp	x26, x25, [sp, #112]            ; 16-byte Folded Spill
	stp	x24, x23, [sp, #128]            ; 16-byte Folded Spill
	stp	x22, x21, [sp, #144]            ; 16-byte Folded Spill
	stp	x20, x19, [sp, #160]            ; 16-byte Folded Spill
	stp	x29, x30, [sp, #176]            ; 16-byte Folded Spill
	add	x29, sp, #176
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
Lloh0:
	adrp	x8, ___stack_chk_guard@GOTPAGE
Lloh1:
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
Lloh2:
	ldr	x8, [x8]
	stur	x8, [x29, #-72]
	mov	w0, #20                         ; =0x14
	bl	__Znwm
	mov	x19, x0
	mov	w8, #5                          ; =0x5
	str	w8, [x0, #16]
Lloh3:
	adrp	x8, l_constinit@PAGE
Lloh4:
	add	x8, x8, l_constinit@PAGEOFF
Lloh5:
	ldr	q0, [x8]
	str	q0, [x0]
Ltmp0:
	mov	w0, #20                         ; =0x14
	bl	__Znwm
Ltmp1:
; %bb.1:
	mov	x20, x0
	stp	xzr, xzr, [x0]
	str	wzr, [x0, #16]
Ltmp3:
	mov	w0, #20                         ; =0x14
	bl	__Znwm
Ltmp4:
; %bb.2:
	mov	x21, x0
	stp	xzr, xzr, [x0]
	str	wzr, [x0, #16]
Ltmp6:
	mov	w0, #20                         ; =0x14
	bl	__Znwm
Ltmp7:
; %bb.3:
	mov	x22, x0
	stp	xzr, xzr, [x0]
	str	wzr, [x0, #16]
Ltmp9:
	mov	w0, #64                         ; =0x40
	bl	__Znwm
Ltmp10:
; %bb.4:
	mov	x23, x0
	movi.2d	v0, #0000000000000000
	stp	q0, q0, [x0, #32]
	stp	q0, q0, [x0]
	add	x1, x19, #20
	mov	x0, x19
	mov	x2, x20
	bl	__Z8copy_stdPKiS0_Pi
	mov	x0, x19
	mov	w1, #5                          ; =0x5
	mov	x2, x21
	bl	__Z11copy_memcpyPKimPi
	mov	x0, x19
	mov	w1, #5                          ; =0x5
	mov	x2, x22
	bl	__Z9copy_loopPKimPi
Ltmp12:
	mov	w0, #64                         ; =0x40
	bl	__Znwm
Ltmp13:
; %bb.5:
	mov	x24, x0
Lloh6:
	adrp	x1, l_.memset_pattern@PAGE
Lloh7:
	add	x1, x1, l_.memset_pattern@PAGEOFF
	mov	w2, #64                         ; =0x40
	bl	_memset_pattern16
	mov	x0, x24
	mov	x1, x23
	bl	__Z12copy_fixed16PKiPi
	mov	w8, #30977                      ; =0x7901
	sturh	w8, [sp, #79]
	mov	w8, #120                        ; =0x78
	strh	w8, [sp, #56]
	mov	w8, #1                          ; =0x1
	strb	w8, [sp, #103]
	strb	wzr, [sp, #81]
	movi.2d	v0, #0000000000000000
	stp	q0, q0, [sp, #16]
	add	x8, sp, #56
	str	q0, [sp]
Ltmp15:
	add	x0, sp, #56
	add	x1, x8, #48
	mov	x2, sp
	bl	__Z12copy_stringsPKNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEES7_PS5_
Ltmp16:
; %bb.6:
	ldr	w1, [x20, #16]
Ltmp17:
Lloh8:
	adrp	x0, __ZNSt3__14coutE@GOTPAGE
Lloh9:
	ldr	x0, [x0, __ZNSt3__14coutE@GOTPAGEOFF]
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi
Ltmp18:
; %bb.7:
	ldr	w1, [x21, #16]
Ltmp19:
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi
Ltmp20:
; %bb.8:
	ldr	w1, [x22, #16]
Ltmp21:
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi
Ltmp22:
; %bb.9:
Ltmp23:
Lloh10:
	adrp	x1, l_.str.2@PAGE
Lloh11:
	add	x1, x1, l_.str.2@PAGEOFF
	mov	w2, #1                          ; =0x1
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp24:
; %bb.10:
	ldr	w1, [x23, #60]
Ltmp25:
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi
Ltmp26:
; %bb.11:
Ltmp27:
Lloh12:
	adrp	x1, l_.str.2@PAGE
Lloh13:
	add	x1, x1, l_.str.2@PAGEOFF
	mov	w2, #1                          ; =0x1
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp28:
; %bb.12:
	mov	x8, sp
	add	x8, x8, #24
	ldrb	w9, [sp, #47]
	sxtb	w10, w9
	ldp	x11, x12, [sp, #24]
	cmp	w10, #0
	csel	x1, x11, x8, lt
	csel	x2, x12, x9, lt
Ltmp29:
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp30:
; %bb.13:
Ltmp31:
Lloh14:
	adrp	x1, l_.str.3@PAGE
Lloh15:
	add	x1, x1, l_.str.3@PAGEOFF
	mov	w2, #1                          ; =0x1
	bl	__ZNSt3__124__put_character_sequenceB9nqe220106IcNS_11char_traitsIcEEEERNS_13basic_ostreamIT_T0_EES7_PKS4_m
Ltmp32:
; %bb.14:
	ldrsb	w8, [sp, #47]
	tbnz	w8, #31, LBB5_20
; %bb.15:
	ldrsb	w8, [sp, #23]
	tbnz	w8, #31, LBB5_21
LBB5_16:
	ldrsb	w8, [sp, #103]
	tbnz	w8, #31, LBB5_22
LBB5_17:
	ldrsb	w8, [sp, #79]
	tbnz	w8, #31, LBB5_23
LBB5_18:
	mov	x0, x24
	bl	__ZdlPv
	mov	x0, x23
	bl	__ZdlPv
	mov	x0, x22
	bl	__ZdlPv
	mov	x0, x21
	bl	__ZdlPv
	mov	x0, x20
	bl	__ZdlPv
	mov	x0, x19
	bl	__ZdlPv
	ldur	x8, [x29, #-72]
Lloh16:
	adrp	x9, ___stack_chk_guard@GOTPAGE
Lloh17:
	ldr	x9, [x9, ___stack_chk_guard@GOTPAGEOFF]
Lloh18:
	ldr	x9, [x9]
	cmp	x9, x8
	b.ne	LBB5_24
; %bb.19:
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #176]            ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #160]            ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #144]            ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #128]            ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #112]            ; 16-byte Folded Reload
	add	sp, sp, #192
	ret
LBB5_20:
	ldr	x0, [sp, #24]
	bl	__ZdlPv
	ldrsb	w8, [sp, #23]
	tbz	w8, #31, LBB5_16
LBB5_21:
	ldr	x0, [sp]
	bl	__ZdlPv
	ldrsb	w8, [sp, #103]
	tbz	w8, #31, LBB5_17
LBB5_22:
	ldr	x0, [sp, #80]
	bl	__ZdlPv
	ldrsb	w8, [sp, #79]
	tbz	w8, #31, LBB5_18
LBB5_23:
	ldr	x0, [sp, #56]
	bl	__ZdlPv
	b	LBB5_18
LBB5_24:
	bl	___stack_chk_fail
LBB5_25:
Ltmp14:
	mov	x25, x0
	b	LBB5_36
LBB5_26:
Ltmp11:
	mov	x25, x0
	b	LBB5_37
LBB5_27:
Ltmp8:
	mov	x25, x0
	b	LBB5_38
LBB5_28:
Ltmp5:
	mov	x25, x0
	b	LBB5_39
LBB5_29:
Ltmp2:
	mov	x25, x0
	b	LBB5_40
LBB5_30:
Ltmp33:
	mov	x25, x0
	ldrsb	w8, [sp, #47]
	tbnz	w8, #31, LBB5_41
; %bb.31:
	ldrsb	w8, [sp, #23]
	tbnz	w8, #31, LBB5_42
LBB5_32:
	ldrsb	w8, [sp, #103]
	tbnz	w8, #31, LBB5_43
LBB5_33:
	ldrsb	w8, [sp, #79]
	tbz	w8, #31, LBB5_35
LBB5_34:
	ldr	x0, [sp, #56]
	bl	__ZdlPv
LBB5_35:
	mov	x0, x24
	bl	__ZdlPv
LBB5_36:
	mov	x0, x23
	bl	__ZdlPv
LBB5_37:
	mov	x0, x22
	bl	__ZdlPv
LBB5_38:
	mov	x0, x21
	bl	__ZdlPv
LBB5_39:
	mov	x0, x20
	bl	__ZdlPv
LBB5_40:
	mov	x0, x19
	bl	__ZdlPv
	mov	x0, x25
	bl	__Unwind_Resume
LBB5_41:
	ldr	x0, [sp, #24]
	bl	__ZdlPv
	ldrsb	w8, [sp, #23]
	tbz	w8, #31, LBB5_32
LBB5_42:
	ldr	x0, [sp]
	bl	__ZdlPv
	ldrsb	w8, [sp, #103]
	tbz	w8, #31, LBB5_33
LBB5_43:
	ldr	x0, [sp, #80]
	bl	__ZdlPv
	ldrsb	w8, [sp, #79]
	tbnz	w8, #31, LBB5_34
	b	LBB5_35
	.loh AdrpAddLdr	Lloh3, Lloh4, Lloh5
	.loh AdrpLdrGotLdr	Lloh0, Lloh1, Lloh2
	.loh AdrpAdd	Lloh6, Lloh7
	.loh AdrpLdrGot	Lloh8, Lloh9
	.loh AdrpAdd	Lloh10, Lloh11
	.loh AdrpAdd	Lloh12, Lloh13
	.loh AdrpAdd	Lloh14, Lloh15
	.loh AdrpLdrGotLdr	Lloh16, Lloh17, Lloh18
Lfunc_end0:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table5:
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
	.uleb128 Ltmp1-Ltmp0                    ;   Call between Ltmp0 and Ltmp1
	.uleb128 Ltmp2-Lfunc_begin0             ;     jumps to Ltmp2
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp3-Lfunc_begin0             ; >> Call Site 3 <<
	.uleb128 Ltmp4-Ltmp3                    ;   Call between Ltmp3 and Ltmp4
	.uleb128 Ltmp5-Lfunc_begin0             ;     jumps to Ltmp5
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp6-Lfunc_begin0             ; >> Call Site 4 <<
	.uleb128 Ltmp7-Ltmp6                    ;   Call between Ltmp6 and Ltmp7
	.uleb128 Ltmp8-Lfunc_begin0             ;     jumps to Ltmp8
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp9-Lfunc_begin0             ; >> Call Site 5 <<
	.uleb128 Ltmp10-Ltmp9                   ;   Call between Ltmp9 and Ltmp10
	.uleb128 Ltmp11-Lfunc_begin0            ;     jumps to Ltmp11
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp12-Lfunc_begin0            ; >> Call Site 6 <<
	.uleb128 Ltmp13-Ltmp12                  ;   Call between Ltmp12 and Ltmp13
	.uleb128 Ltmp14-Lfunc_begin0            ;     jumps to Ltmp14
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp15-Lfunc_begin0            ; >> Call Site 7 <<
	.uleb128 Ltmp32-Ltmp15                  ;   Call between Ltmp15 and Ltmp32
	.uleb128 Ltmp33-Lfunc_begin0            ;     jumps to Ltmp33
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp32-Lfunc_begin0            ; >> Call Site 8 <<
	.uleb128 Lfunc_end0-Ltmp32              ;   Call between Ltmp32 and Lfunc_end0
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
	.globl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm ; -- Begin function _ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm
	.weak_def_can_be_hidden	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm
	.p2align	2
__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm: ; @_ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb0EEERS5_PKcm
	.cfi_startproc
; %bb.0:
	stp	x22, x21, [sp, #-48]!           ; 16-byte Folded Spill
	stp	x20, x19, [sp, #16]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	mov	x20, x2
	mov	x7, x1
	mov	x19, x0
	ldr	x8, [x0, #16]
	and	x9, x8, #0x7fffffffffffffff
	subs	x8, x2, x9
	b.hs	LBB7_2
; %bb.1:
	ldr	x21, [x19]
	str	x20, [x19, #8]
	mov	x0, x21
	mov	x1, x7
	mov	x2, x20
	bl	_memmove
	strb	wzr, [x21, x20]
	b	LBB7_3
LBB7_2:
	ldr	x3, [x19, #8]
	sub	x1, x9, #1
	add	x2, x8, #1
	mov	x0, x19
	mov	x4, #0                          ; =0x0
	mov	x5, x3
	mov	x6, x20
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE21__grow_by_and_replaceEmmmmmmPKc
LBB7_3:
	mov	x0, x19
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #16]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp], #48             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm ; -- Begin function _ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm
	.weak_def_can_be_hidden	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm
	.p2align	2
__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm: ; @_ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE17__assign_no_aliasILb1EEERS5_PKcm
	.cfi_startproc
; %bb.0:
	stp	x20, x19, [sp, #-32]!           ; 16-byte Folded Spill
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	mov	x20, x2
	mov	x7, x1
	mov	x19, x0
	cmp	x2, #23
	b.lo	LBB8_2
; %bb.1:
	ldrb	w8, [x19, #23]
	sub	x2, x20, #22
	and	x3, x8, #0x7f
	and	x5, x8, #0x7f
	mov	x0, x19
	mov	w1, #22                         ; =0x16
	mov	x4, #0                          ; =0x0
	mov	x6, x20
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE21__grow_by_and_replaceEmmmmmmPKc
	b	LBB8_3
LBB8_2:
	strb	w20, [x19, #23]
	mov	x0, x19
	mov	x1, x7
	mov	x2, x20
	bl	_memmove
	strb	wzr, [x19, x20]
LBB8_3:
	mov	x0, x19
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp], #32             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
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
Lloh19:
	adrp	x0, l_.str.4@PAGE
Lloh20:
	add	x0, x0, l_.str.4@PAGEOFF
	bl	__ZNSt3__120__throw_length_errorB9nqe220106EPKc
	.loh AdrpAdd	Lloh19, Lloh20
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
Ltmp34:
	mov	x1, x20
	bl	__ZNSt12length_errorC1B9nqe220106EPKc
Ltmp35:
; %bb.1:
Lloh21:
	adrp	x1, __ZTISt12length_error@GOTPAGE
Lloh22:
	ldr	x1, [x1, __ZTISt12length_error@GOTPAGEOFF]
Lloh23:
	adrp	x2, __ZNSt12length_errorD1Ev@GOTPAGE
Lloh24:
	ldr	x2, [x2, __ZNSt12length_errorD1Ev@GOTPAGEOFF]
	mov	x0, x19
	bl	___cxa_throw
LBB10_2:
Ltmp36:
	mov	x20, x0
	mov	x0, x19
	bl	___cxa_free_exception
	mov	x0, x20
	bl	__Unwind_Resume
	.loh AdrpLdrGot	Lloh23, Lloh24
	.loh AdrpLdrGot	Lloh21, Lloh22
Lfunc_end1:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table10:
Lexception1:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	255                             ; @TType Encoding = omit
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end1-Lcst_begin1
Lcst_begin1:
	.uleb128 Lfunc_begin1-Lfunc_begin1      ; >> Call Site 1 <<
	.uleb128 Ltmp34-Lfunc_begin1            ;   Call between Lfunc_begin1 and Ltmp34
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp34-Lfunc_begin1            ; >> Call Site 2 <<
	.uleb128 Ltmp35-Ltmp34                  ;   Call between Ltmp34 and Ltmp35
	.uleb128 Ltmp36-Lfunc_begin1            ;     jumps to Ltmp36
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp35-Lfunc_begin1            ; >> Call Site 3 <<
	.uleb128 Lfunc_end1-Ltmp35              ;   Call between Ltmp35 and Lfunc_end1
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
Lloh25:
	adrp	x8, __ZTVSt12length_error@GOTPAGE
Lloh26:
	ldr	x8, [x8, __ZTVSt12length_error@GOTPAGEOFF]
	add	x8, x8, #16
	str	x8, [x0]
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.loh AdrpLdrGot	Lloh25, Lloh26
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
Ltmp37:
	add	x0, sp, #8
	mov	x1, x19
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryC1ERS3_
Ltmp38:
; %bb.1:
	ldrb	w8, [sp, #8]
	cmp	w8, #1
	b.ne	LBB12_10
; %bb.2:
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
	add	x4, x19, x8
	ldr	x22, [x4, #40]
	ldr	w24, [x4, #8]
	ldr	w23, [x4, #144]
	cmn	w23, #1
	b.ne	LBB12_7
; %bb.3:
Ltmp40:
	add	x8, sp, #24
	mov	x25, x4
	mov	x0, x4
	bl	__ZNKSt3__18ios_base6getlocEv
Ltmp41:
; %bb.4:
Ltmp42:
Lloh27:
	adrp	x1, __ZNSt3__15ctypeIcE2idE@GOTPAGE
Lloh28:
	ldr	x1, [x1, __ZNSt3__15ctypeIcE2idE@GOTPAGEOFF]
	add	x0, sp, #24
	bl	__ZNKSt3__16locale9use_facetERNS0_2idE
Ltmp43:
; %bb.5:
	ldr	x8, [x0]
	ldr	x8, [x8, #56]
Ltmp44:
	mov	w1, #32                         ; =0x20
	blr	x8
Ltmp45:
; %bb.6:
	mov	x23, x0
	add	x0, sp, #24
	bl	__ZNSt3__16localeD1Ev
	mov	x4, x25
	str	w23, [x25, #144]
LBB12_7:
	mov	w8, #176                        ; =0xb0
	and	w8, w24, w8
	add	x3, x20, x21
	cmp	w8, #32
	csel	x2, x3, x20, eq
Ltmp47:
	sxtb	w5, w23
	mov	x0, x22
	mov	x1, x20
	bl	__ZNSt3__116__pad_and_outputB9nqe220106IcNS_11char_traitsIcEEEENS_19ostreambuf_iteratorIT_T0_EES6_PKS4_S8_S8_RNS_8ios_baseES4_
Ltmp48:
; %bb.8:
	cbnz	x0, LBB12_10
; %bb.9:
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
	add	x0, x19, x8
	ldr	w8, [x0, #32]
	mov	w9, #5                          ; =0x5
Ltmp50:
	orr	w1, w8, w9
	bl	__ZNSt3__18ios_base5clearEj
Ltmp51:
LBB12_10:
	add	x0, sp, #8
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryD1Ev
LBB12_11:
	mov	x0, x19
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #80]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #64]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #48]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #112
	ret
LBB12_12:
Ltmp52:
	b	LBB12_15
LBB12_13:
Ltmp46:
	mov	x20, x0
	add	x0, sp, #24
	bl	__ZNSt3__16localeD1Ev
	b	LBB12_16
LBB12_14:
Ltmp49:
LBB12_15:
	mov	x20, x0
LBB12_16:
	add	x0, sp, #8
	bl	__ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryD1Ev
	b	LBB12_18
LBB12_17:
Ltmp39:
	mov	x20, x0
LBB12_18:
	mov	x0, x20
	bl	___cxa_begin_catch
	ldr	x8, [x19]
	ldur	x8, [x8, #-24]
Ltmp53:
	add	x0, x19, x8
	bl	__ZNSt3__18ios_base33__set_badbit_and_consider_rethrowEv
Ltmp54:
; %bb.19:
	bl	___cxa_end_catch
	b	LBB12_11
LBB12_20:
Ltmp55:
	mov	x19, x0
Ltmp56:
	bl	___cxa_end_catch
Ltmp57:
; %bb.21:
	mov	x0, x19
	bl	__Unwind_Resume
LBB12_22:
Ltmp58:
	bl	___clang_call_terminate
	.loh AdrpLdrGot	Lloh27, Lloh28
Lfunc_end2:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table12:
Lexception2:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	155                             ; @TType Encoding = indirect pcrel sdata4
	.uleb128 Lttbase0-Lttbaseref0
Lttbaseref0:
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end2-Lcst_begin2
Lcst_begin2:
	.uleb128 Ltmp37-Lfunc_begin2            ; >> Call Site 1 <<
	.uleb128 Ltmp38-Ltmp37                  ;   Call between Ltmp37 and Ltmp38
	.uleb128 Ltmp39-Lfunc_begin2            ;     jumps to Ltmp39
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp40-Lfunc_begin2            ; >> Call Site 2 <<
	.uleb128 Ltmp41-Ltmp40                  ;   Call between Ltmp40 and Ltmp41
	.uleb128 Ltmp49-Lfunc_begin2            ;     jumps to Ltmp49
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp42-Lfunc_begin2            ; >> Call Site 3 <<
	.uleb128 Ltmp45-Ltmp42                  ;   Call between Ltmp42 and Ltmp45
	.uleb128 Ltmp46-Lfunc_begin2            ;     jumps to Ltmp46
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp47-Lfunc_begin2            ; >> Call Site 4 <<
	.uleb128 Ltmp48-Ltmp47                  ;   Call between Ltmp47 and Ltmp48
	.uleb128 Ltmp49-Lfunc_begin2            ;     jumps to Ltmp49
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp50-Lfunc_begin2            ; >> Call Site 5 <<
	.uleb128 Ltmp51-Ltmp50                  ;   Call between Ltmp50 and Ltmp51
	.uleb128 Ltmp52-Lfunc_begin2            ;     jumps to Ltmp52
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp51-Lfunc_begin2            ; >> Call Site 6 <<
	.uleb128 Ltmp53-Ltmp51                  ;   Call between Ltmp51 and Ltmp53
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp53-Lfunc_begin2            ; >> Call Site 7 <<
	.uleb128 Ltmp54-Ltmp53                  ;   Call between Ltmp53 and Ltmp54
	.uleb128 Ltmp55-Lfunc_begin2            ;     jumps to Ltmp55
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp54-Lfunc_begin2            ; >> Call Site 8 <<
	.uleb128 Ltmp56-Ltmp54                  ;   Call between Ltmp54 and Ltmp56
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp56-Lfunc_begin2            ; >> Call Site 9 <<
	.uleb128 Ltmp57-Ltmp56                  ;   Call between Ltmp56 and Ltmp57
	.uleb128 Ltmp58-Lfunc_begin2            ;     jumps to Ltmp58
	.byte	1                               ;   On action: 1
	.uleb128 Ltmp57-Lfunc_begin2            ; >> Call Site 10 <<
	.uleb128 Lfunc_end2-Ltmp57              ;   Call between Ltmp57 and Lfunc_end2
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
	cbz	x0, LBB13_16
; %bb.1:
	mov	x23, x5
	mov	x20, x4
	mov	x22, x3
	mov	x21, x2
	mov	x24, x1
	ldr	x26, [x4, #24]
	sub	x25, x2, x1
	cmp	x25, #1
	b.lt	LBB13_3
; %bb.2:
	ldr	x8, [x19]
	ldr	x8, [x8, #96]
	mov	x0, x19
	mov	x1, x24
	mov	x2, x25
	blr	x8
	cmp	x0, x25
	b.ne	LBB13_15
LBB13_3:
	sub	x8, x22, x24
	cmp	x26, x8
	b.le	LBB13_12
; %bb.4:
	mov	x9, #-9                         ; =0xfffffffffffffff7
	movk	x9, #32767, lsl #48
	sub	x24, x26, x8
	cmp	x24, x9
	b.hs	LBB13_17
; %bb.5:
	cmp	x24, #23
	b.hs	LBB13_7
; %bb.6:
	strb	w24, [sp, #31]
	add	x25, sp, #8
	b	LBB13_8
LBB13_7:
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
LBB13_8:
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
Ltmp59:
	mov	x0, x19
	mov	x2, x24
	blr	x8
Ltmp60:
; %bb.9:
	ldrsb	w8, [sp, #31]
	tbnz	w8, #31, LBB13_11
; %bb.10:
	cmp	x0, x24
	b.ne	LBB13_15
	b	LBB13_12
LBB13_11:
	ldr	x8, [sp, #8]
	mov	x23, x0
	mov	x0, x8
	bl	__ZdlPv
	mov	x0, x23
	cmp	x0, x24
	b.ne	LBB13_15
LBB13_12:
	sub	x22, x22, x21
	cmp	x22, #1
	b.lt	LBB13_14
; %bb.13:
	ldr	x8, [x19]
	ldr	x8, [x8, #96]
	mov	x0, x19
	mov	x1, x21
	mov	x2, x22
	blr	x8
	cmp	x0, x22
	b.ne	LBB13_15
LBB13_14:
	str	xzr, [x20, #24]
	b	LBB13_16
LBB13_15:
	mov	x19, #0                         ; =0x0
LBB13_16:
	mov	x0, x19
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #80]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #64]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #48]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #112
	ret
LBB13_17:
	bl	__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE20__throw_length_errorB9nqe220106Ev
LBB13_18:
Ltmp61:
	mov	x19, x0
	ldrsb	w8, [sp, #31]
	tbz	w8, #31, LBB13_20
; %bb.19:
	ldr	x0, [sp, #8]
	bl	__ZdlPv
LBB13_20:
	mov	x0, x19
	bl	__Unwind_Resume
Lfunc_end3:
	.cfi_endproc
	.section	__TEXT,__gcc_except_tab
	.p2align	2, 0x0
GCC_except_table13:
Lexception3:
	.byte	255                             ; @LPStart Encoding = omit
	.byte	255                             ; @TType Encoding = omit
	.byte	1                               ; Call site Encoding = uleb128
	.uleb128 Lcst_end3-Lcst_begin3
Lcst_begin3:
	.uleb128 Lfunc_begin3-Lfunc_begin3      ; >> Call Site 1 <<
	.uleb128 Ltmp59-Lfunc_begin3            ;   Call between Lfunc_begin3 and Ltmp59
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp59-Lfunc_begin3            ; >> Call Site 2 <<
	.uleb128 Ltmp60-Ltmp59                  ;   Call between Ltmp59 and Ltmp60
	.uleb128 Ltmp61-Lfunc_begin3            ;     jumps to Ltmp61
	.byte	0                               ;   On action: cleanup
	.uleb128 Ltmp60-Lfunc_begin3            ; >> Call Site 3 <<
	.uleb128 Lfunc_end3-Ltmp60              ;   Call between Ltmp60 and Lfunc_end3
	.byte	0                               ;     has no landing pad
	.byte	0                               ;   On action: cleanup
Lcst_end3:
	.p2align	2, 0x0
                                        ; -- End function
	.section	__TEXT,__const
	.p2align	2, 0x0                          ; @constinit
l_constinit:
	.long	1                               ; 0x1
	.long	2                               ; 0x2
	.long	3                               ; 0x3
	.long	4                               ; 0x4
	.long	5                               ; 0x5

	.section	__TEXT,__cstring,cstring_literals
l_.str.2:                               ; @.str.2
	.asciz	" "

l_.str.3:                               ; @.str.3
	.asciz	"\n"

l_.str.4:                               ; @.str.4
	.asciz	"basic_string"

	.section	__TEXT,__literal16,16byte_literals
	.p2align	4, 0x0                          ; @.memset_pattern
l_.memset_pattern:
	.long	7                               ; 0x7
	.long	7                               ; 0x7
	.long	7                               ; 0x7
	.long	7                               ; 0x7

.subsections_via_symbols
