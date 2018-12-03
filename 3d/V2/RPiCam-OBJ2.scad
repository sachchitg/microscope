// ==============================================
// Microscope Objective mount for Raspberry Pi camera
// using AmScope 4x http://www.ebay.com/itm/381613828736
// Also, model of Raspberry Pi Camera v2.1
// connects to RPi PCB using 4x M2 screws + nuts
//
// J.Beale 15-May-2016
// ==============================================

xs = 25.0;  // width of PCB
ys = 23.85;  // height of PCB
zs = 0.95;  // thickness of bare PCB, not including soldermask
smt = 0.05;  // soldermask thickness (on each side)

ID1 = 2.20; // ID of mounting through-holes
OD1 = 4.7;  // silkscreen clearance around hole
ID2 = 2.0; // ID of mounting through-holes

mhxc = 21.0;  // X center-to-center separation of mounting holes
mhyc = 12.5; // Y center-to-center separation of mtng. holes
mhox = 2.0;  // X mounting hole corner offset
mhoy = 2.0;  // Y mounting hole corner offset
hh = zs*2; // depth/height of mounting hole (subtractive cylinder)

smx = 8.45;  // camera sensor module, base part
smy = 8.45;
smz = 2.3;
smbod = 7.25;  // OD of lens holder barrel
smbz = 1.7; // z-height of lens holder barrel
smcod = 5.6;  // OD of lens cell 
smcz = 0.6;  // protrusion of cell above holder barrel
smcid = 1.55;  // optical aperture: opening for lens

smfx = 8.9; // flex connector width
smfy = 4.5; // flex connector 
smfz = 1.52; // flex connector
smfox = 9.45; // flex edge X offset
smfoy = 2.6; // flex edge Y offset
smfcx = 7.2; // flex cable width

fcy = 5.8; // 15-way flex connector
fcx = 21.0; // 15-way flex connector
fcz = 3.77-1.15; // 15-way flex connector height  
fcyoff = 0.3; // connector offset from PCB edge

ffx = 16.05;  // 15-way flex cable width
ffy = 30;  // length of flex cable stub
ffz = 0.38;  // thickness of ff cable at stiffener
ffoz = 1.1; // offset of ff cable below PCB

KOx = 22.15; // keepout width- full
KOxa = 15.1; // keepout width- inner block
KOz = 1.35; // bottom side keepout z-height
KOyo = 1.15; // keepout edge offset
// ==============================================

ff = 0.2;  // amount to increase ID due to printer slop

MOd = 22.0+ff;  // OD of AmScope 4x microscope objective
MOz = 13;    // length of constant-OD part of objective barrel
MOoff = 7.3;  // height offset of objective
// MOoff = -10;  // height offset of objective
MOda = 22.5+ff;  // OD of 2nd barrel part
MOza = 5.0;  // height of 2nd barrel part

BHwt = 2.0;  // wall thickness of objective barrel holder
BHz = MOz+4;  // wall thickness of objective barrel holder
BHod = MOd+2*BHwt; // OD of OBJ barrell holder
BHod2 = 19; // OD of bottom of support cone
// ===============================================

module holes4(dia=2.2,ht=9.5) {
 translate([mhox,mhoy,-zs*5]) {  // through holes
  cylinder(d=dia,h=ht,$fn=fn);     
  translate([mhxc,0,0])  cylinder(d=dia,h=ht,$fn=fn);
  translate([mhxc,mhyc,0])  cylinder(d=dia,h=ht,$fn=fn);
  translate([0,mhyc,0])  cylinder(d=dia,h=ht,$fn=fn);
  }
}
// -------------------------------------
  
module MicObj() {  // lower part of one 4x objective
 translate([xs/2,mhyc+mhoy,MOoff]) union() {
  cylinder(d=MOd, h=MOz, $fn=fn*2);
  translate([0,0,MOz-eps]) cylinder(d=MOda, h=MOza, $fn=fn*2);
 }
}
// %MicObj();

module ObjHolder() {


 difference() { 
 union() {
  translate([xs/2,mhyc+mhoy,eps]) 
    cylinder(d1=BHod2, d2=BHod, h=MOoff, $fn=fn*2);
    cube([xs,ys,3]);  // square base of holder
    translate([5,0,0]) cube([15,15,5]); // side extension over micro-flex
 }
 holes4(2.0);
 translate([0,0,7.5]) holes4(OD1+0.5,2.5);
 translate([xs/2,mhyc+mhoy,-eps]) // tapered cylinder part
  cylinder(d1=BHod2-3*BHwt, d2=BHod-5*BHwt, h=MOoff+4*eps, $fn=fn*2);
 translate([xs/2,mhyc+mhoy,eps])
   translate([-3.8,-13,-0.5]) cube([10,10,4]); // notch for micro-flex
 }
 
difference() { // stright cylinder part
 translate([xs/2,mhyc+mhoy,MOoff+eps])
  cylinder(d=BHod, h= BHz, $fn=fn*2);
 translate([xs/2,-2,MOoff+eps+5]) 
     cube([1,BHod*2,BHz]); // slot across top

 MicObj();
}
}

translate([0,0,zs+(2*smt)]) ObjHolder();  // <= Objective Holder Assy

/*
%difference() {
translate([0,0,zs+(2*smt)]) ObjHolder();
translate([10,10,0]) cube([100,100,100]);
} */

// ==============================================

fn=4000;  // facets on cylinder
eps=0.03; // small number

// ---------------------------------
// PCB holding camera module v2.1
module pcb() {
difference() {
 union() {
     translate([0,0,0]) color("green") 
        cube([xs,ys,smt]); // soldermask (bottom)
     translate([0,0,smt]) color("yellow") 
        cube([xs,ys,zs]); // natural PCB color
     translate([0,0,zs]) color("green") 
        cube([xs,ys,smt]); // soldermask (top)
 }
 translate([mhox,mhoy,zs-(smt+eps)]) {  // mask clearance: top
     cylinder(d=OD1,h=zs,$fn=fn);
     translate([mhxc,0,0]) cylinder(d=OD1,h=zs,$fn=fn);
     translate([mhxc,mhyc,0]) cylinder(d=OD1,h=zs,$fn=fn);
     translate([0,mhyc,0]) cylinder(d=OD1,h=zs,$fn=fn);
 }
 translate([mhox,mhoy,-eps]) {  // mask clearance: bottom
     cylinder(d=OD1,h=smt,$fn=fn);
     translate([mhxc,0,0]) cylinder(d=OD1,h=smt,$fn=fn);
     translate([mhxc,mhyc,0]) cylinder(d=OD1,h=smt,$fn=fn);
     translate([0,mhyc,0]) cylinder(d=OD1,h=smt,$fn=fn);
 }
 holes4(ID1);  // 4x mounting holes
 }
}


module sensor() { // Camera sensor module
 color([.25,.25,.25]) translate([-smx/2, -smy/2, 0]) cube([smx,smy,smz]);
 color([.3,.3,.3]) cylinder(d=smbod, h=smbz + smz, $fn=fn);
 difference() {
  color([.2,.2,.2]) cylinder(d=smcod, h=smbz + smz + smcz, $fn=fn);
  translate([0,0,smcz]) cylinder(d=smcid, h=smbz + smz + smcz, $fn=fn);
 }
}

module flex() { // micro-flex attached to sensor
 color([0.2,0.20,0.18]) cube([smfx,smfy,smfz]); // u-flex connector top
 translate([0,smfy,0]) color([0.33,0.33,0.23]) cube([smfcx,smfy,smfz-.1]);
}

module fcon() {  // micro-flex connector to PCB
    color([0.6,0.20,0.18]) cube([fcx,fcy,fcz]);
}

module ff15() {  // 15-conductor flat flex cable
    color([.7,.7,.7]) cube([ffx,ffy,ffz]);
}

KOx = 22.3; // keepout width- full
KOxa = 15.1; // keepout width- inner block
KOy = 22.87-fcy;  // keepout height
KOya = 4.7;  // keepout height
KOz = 1.3; // bottom side keepout z-height
KOyo = 1.15; // keepout edge offset
KOxo = 1.54; // keepout 2nd-block X edge offset
KOyoa = 6.5; // keepout 2nd-block Y edge offset

module keepout() {
  translate([(xs-KOxa)/2,ys-(KOy+fcy),-KOz])  cube([KOxa,KOy,KOz]);
  translate([KOxo,KOyoa,-KOz])  cube([KOx,KOya,KOz]);    
}

// ---------------------------------------------

module cam_full() { // top, bottom & flex cable stub
  translate([xs/2 ,mhyc+mhoy,zs]) sensor();
  pcb();
  translate([smfox,smfoy,zs]) flex(); // micro-flex on sensor

  color([0.7,0.1,0.1])  keepout();  // bottom side circuits
  translate([(xs-fcx)/2,ys-fcy-fcyoff,-fcz]) fcon();  // FF15 flex connector
  translate([(xs-ffx)/2,ys-fcyoff,-ffoz]) ff15();  // FF15 flex cable
}

module cam_top() {  // only topside components
  translate([xs/2 ,mhyc+mhoy,zs]) sensor();
  pcb();
  translate([smfox,smfoy,zs]) flex(); // micro-flex on sensor
}

//cam_top();
//cam_full();
