include <ISOThreadLeg.scad>

$fn=100;
module derlin_nut(){
    difference() {
        cube([35,20,13]);
        
        M5 = 0.9927*5 + 0.3602;
        M8 = 1.0155*8 + 0.2795;
        M9 = 0.9927*9 + 0.3602;
        
        ThreadM8 = 1.0155*8 + 0.2795;
        
       translate ([7.5,10,11]) {
            cylinder (h = 4.1, d=M9, center = true, $fn=6);
            }
       translate ([27.5,10,11]) {
            cylinder (h = 4.1, d=M9, center = true, $fn=6);
            }
       translate ([7.5,10,-4]) {
            cylinder (d=M5, h=100, center=true);
            }
        translate ([27.5,10,-4]) {
            cylinder (d=M5, h=100, center=true);
            }
        translate ([17.5,35,6.5]) {
             rotate ([90,0,0]) cylinder (d=M8, h=100,center=true);
            }
    }
     translate ([17.5,20,6.5]) {
             rotate ([90,0,0]) thread_in(8.4035,20);
     }
}

rotate([90,0,0]){
derlin_nut();}