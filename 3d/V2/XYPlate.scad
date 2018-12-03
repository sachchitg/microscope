include <ISOThreadLeg.scad>

$fn=100;
module plate(){
    difference() {
            cube([75,75,5]);
        
        translate ([8.75,45,3]) {
            cube([35.1,20.1,13]);
        }
        
        translate ([46,40,3]) {
            cube([20.1,29,8]);
        }
        
        translate ([-10,22,-11.5]) {
            cube([300,15,15]);
        }
        
        translate ([-10,4,-11.5]) {
            cube([300,15,15]);
        }
        
        translate ([15,29.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([30,29.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([45,29.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([60,29.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([15,11.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([30,11.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([45,11.5,-20]) {
           cylinder (r=1.5, h=100);
        }
        
        translate ([60,11.5,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([48.5,49.45,-20]) {
           cylinder (r=1.5, h=100);
        }
        
        translate ([48.5,59.45,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([63.5,49.45,-20]) {
            cylinder (r=1.5, h=100);
        }
        
        translate ([63.5,59.45,-20]) {
            cylinder (r=1.5, h=100);
        }
        
       translate ([16.25,55,-20]) {
            cylinder (r=2.5, h=100);
            }
            
       translate ([36.25,55,-20]) {
            cylinder (r=2.5, h=100);
            }
    }
}

plate();
