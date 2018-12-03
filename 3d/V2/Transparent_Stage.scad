$fn=1000;
module plate(x,y){
       translate ([x,y]) { 
           difference() {
             square([150,150]);
               
            cx = 150/2;
            cy = 150-7.5;
            M3 = 3 + 0.15;
            M5 = 5 + 0.15;
            
            clipx = 30;
            clipy = 95;
            
            translate ([cx-3*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+3*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+5.5,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+71,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+71+22.5,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+7,clipy-34]) {
                square ([68,22]);
            }
            
            
        cyleft = 150/2;
        cxleft = 7.5;
       
       translate ([cxleft,cyleft-2*15]) {
                circle (d=M3, center=true);
            }
           
            translate ([cxleft,cyleft-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
 
        cxright = 150-7.5;
       
       translate ([cxright,cyleft-2*15]) {
                circle (d=M3, center=true);
            }
           
            translate ([cxright,cyleft-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([0,150-15]) {
                square ([40,16]);
            }
            
            translate ([150-40,150-15]) {
                square ([41,16]);
            }
        }
    }
}

module platev2(x,y){
       translate ([x,y]) { 
           difference() {
             square([150,150]);
               
            cx = 150/2;
            cy = 150-7.5;
            M3 = 3 + 0.15;
            M5 = 5 + 0.15;
            
            clipx = 30;
            clipy = 95;
            
            translate ([cx-4*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+4*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+5.5,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+71,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+71+22.5,clipy]) {
                circle (d=M3, center=true);
            }
            
            translate ([clipx+7,clipy-34]) {
                square ([68,22]);
            }
            
            
        cyleft = 150/2;
        cxleft = 7.5;
       
       translate ([cxleft,cyleft-2*15]) {
                circle (d=M3, center=true);
            }
           
            translate ([cxleft,cyleft-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
 
        cxright = 150-7.5;
       
       translate ([cxright,cyleft-2*15]) {
                circle (d=M3, center=true);
            }
           
            translate ([cxright,cyleft-15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
            
            translate ([40-15,150-15]) {
                square ([15,16]);
            }
            
            translate ([150-40,150-15]) {
                square ([15,16]);
            }
        }
    }
}

module light(){
    difference() {
        square([100,100]);
        cx = 100/2;
        cy = 100-7.5;
        M3 = 3 + 0.15;
        
            
            translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([50,70]) {
                circle (d=14+0.15, center=true);
            }
            
            translate ([70,17.5]) {
                circle (d=7+ 0.15, center=true);
            }
            
            translate([70+10,7.5]) {
                 square([13,20]);
            }
        }
}

module light1(){
    difference() {
        square([100,100]);
        cx = 100/2;
        cy = 100-7.5;
        M3 = 3 + 0.15;
        
            
            translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
                    translate ([50,75]) {
                circle (d=25+0.15, center=true);
            }
            
            translate ([70,17.5]) {
                circle (d=7+ 0.15, center=true);
            }
            
            translate([70+10,7.5]) {
                 square([13,20]);
            }
        }
}

module extension_holder(){
    difference() {
        square([200,120]);
        M8 = 8 + 0.15;
        c8x = 13.5;
        c8y = 120/2;
        translate ([c8x,c8y]) {
                circle (d=M8, center=true);
        }
            
        translate ([c8x+173,c8y]) {
                circle (d=M8, center=true);
       }
       
       cx = 200/2;
        cy = 120-7.5;
        M3 = 3 + 0.15;
       
       translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
         clx = 200/2;
        cly = 7.5;
        M3 = 3 + 0.15;
       
       translate ([clx-2*15,cly]) {
                circle (d=M3, center=true);
            }
           
            translate ([clx-15,cly]) {
                circle (d=M3, center=true);
            }
            
            translate ([clx,cly]) {
                circle (d=M3, center=true);
            }
            
            translate ([clx+15,cly]) {
                circle (d=M3, center=true);
            }
            
            translate ([clx+2*15,cly]) {
                circle (d=M3, center=true);
            }
    }
}

module light_reflect(){
           difference() {
             square([150,150]);
               
            cx = 150/2;
            cy = 150-7.5;
            M3 = 3 + 0.15;
            
            translate ([cx-3*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx-2*15,cy]) {
                circle (d=M3, center=true);
            }
           
            translate ([cx-15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+2*15,cy]) {
                circle (d=M3, center=true);
            }
            
            translate ([cx+3*15,cy]) {
                circle (d=M3, center=true);
            }
            
            
            
        cyleft = 150/2+20;
        cxleft = 7.5;
            
            translate ([cxleft,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxleft,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
 
        cxright = 150-7.5;
       
            
            translate ([cxright,cyleft]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+15]) {
                circle (d=M3, center=true);
            }
            
            translate ([cxright,cyleft+2*15]) {
                circle (d=M3, center=true);
            }
        }
}

platev2(0,0);
plate(151,0);
//translate ([0,151]) {
//light();
//}
//translate ([151,0]) {
//light_reflect();
//}
//translate ([252,0]) {
//light1();
//}
//translate ([0,151]) {
//extension_holder();
//}
//translate ([201,151]) {
//light();
//}