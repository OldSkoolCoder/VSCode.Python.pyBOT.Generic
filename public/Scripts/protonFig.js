    // var protonFig_c = document.getElementById('protonFig_canvas');
    // var protonFig_c = protonFig_protonFigCTX.getContext('2d');
    // var SIN = Math.sin;
    // function wave(a,b) { return (SIN(b*0.11)+SIN((a+(b*0.2))*0.15)); }
  
    // // var zs = 900, zd = 1000, zc = zs-400;
    // // // var bg_w = 800, bg_h = 600; 
    // // var bg_w = 1920, bg_h = 1080; 
    // // var sc_l = 0, sc_t = -40, sc_f = 0;
    // // var adj_y = -35;
    // // setInterval(function(){bg_fx();}, 25);

    // var zs = 1200, zd = 42, zc = zs+300;
    // var bg_w = 800, bg_h = 600; 
    // var sc_l = 0, sc_t = -40, sc_f = 0;
    // var adj_y = -100;
    // setInterval(function(){bg_fx();}, 50);

    // function bg_fx() {
    //   protonFig_protonFigCTX.fillStyle="rgb(192,224,255)";
    //   protonFig_protonFigCTX.fillRect(0,0, bg_w, bg_h);
    //   sc_f -= 1;
    //   sc_l += 1;
    //   var clw = .5;
    //   var sc = bg_w / zd;
    //   var sh_l = (sc_l%1) * zd; 
    //   var sh_f = (sc_f%1) * zd;
    //   for (var sz = 100; sz >= 10; sz--) {
    //     clw += 0.025;
    //     var ew = sz*.8;
    //     var zpos = (sz*zd)-sh_f; 
    //     var sv = false;
    //     var fp = true;
    //     var co = (-zc+sz*20);
    //     var rc = (255-co);
    //     if (co>zc) co= zc-(co-zc);
    //     protonFig_protonFigCTX.strokeStyle = "rgb("+co+","+co/2+","+rc+")"; 	
    //     protonFig_protonFigCTX.beginPath();
    //     protonFig_protonFigCTX.lineWidth = clw;
    //     for(var sx = -ew; sx<=sc+ew; sx++) {
    //       var wfx = (wave(sx*3.1+sc_l*2,sc_f*1.3+sz*1.17)*3+wave(sx*2.5+sc_l*1.4,sc_f*.5+sz*1.3)*5+wave(sx*1.3+sc_l*1.2,sc_f*2.13+sz)*7)/3;
    //       var xpos = (sx*zd*1.1)-sh_l*2+wave(sx*2.5+sc_l*0.5,sc_f*0.6+sz*2.5)*50;
    //       var ypos = (wfx-sc_t)*zd*0.7;
    //       var scale = zs/(zs+zpos);
    //       var x2d = ((xpos-bg_w/2) * scale) + bg_w/2;
    //       var y2d = ((ypos) * scale) + adj_y - (zpos*0.01);
    //       if (y2d > bg_h) y2d = bg_h;
    //       else if (y2d < 0) y2d = 0;
    //       else sv = true;
    //       if (fp) protonFig_protonFigCTX.moveTo(x2d, y2d);
    //       else protonFig_protonFigCTX.lineTo(x2d, y2d);
    //       fp = false;
    //     }
    //     if (sv) protonFig_protonFigCTX.stroke();
    //   }
    // }


    



    function livebg() {
        var protonFigCanvas = document.getElementById('protonFig_canvas');
        var protonFigCTX = protonFigCanvas.getContext('2d');
        var SIN = Math.sin;
        function wave(a,b) { return (SIN(b*0.11)+SIN((a+(b*0.2))*0.15)); }
      
        var zs = 1200, zd = 60, zc = zs-200;
        var bg_w = 1450, bg_h = 1000; 
        var sc_l = 0, sc_t = -40, sc_f = 0;
        var adj_y = -100;
        setInterval(function(){bg_fx();}, 50);
      
        function bg_fx() {
          protonFigCTX.fillStyle="rgb(255,224,192)";
          protonFigCTX.fillRect(0,0, bg_w, bg_h);
          sc_f -= 1;
          sc_l += 1;
          var clw = .5;
          var sc = bg_w / zd;
          var sh_l = (sc_l%1) * zd; 
          var sh_f = (sc_f%1) * zd;
          for (var sz = 200; sz >= 10; sz--) {
            clw += 0.035;
            var ew = sz*.8;
            var zpos = (sz*zd)-sh_f; 
            var sv = false;
            var fp = true;
            var co = (-zc+sz*30);
            var rc = (255-co);
            if (co>zc) co= zc-(co-zc);
            protonFigCTX.strokeStyle = "rgb("+co+","+co/2+","+rc+")"; 	
            protonFigCTX.beginPath();
            protonFigCTX.lineWidth = clw;
            for(var sx = -ew; sx<=sc+ew; sx++) {
              var wfx = (wave(sx*3.1+sc_l*2,sc_f*1.3+sz*1.17)*3+wave(sx*2.5+sc_l*1.4,sc_f*.5+sz*1.3)*5+wave(sx*1.3+sc_l*1.2,sc_f*2.13+sz)*7)/3;
              var xpos = (sx*zd*1.1)-sh_l*2+wave(sx*2.5+sc_l*0.5,sc_f*0.6+sz*2.5)*50;
              var ypos = (wfx-sc_t)*zd*0.7;
              var scale = zs/(zs+zpos);
              var x2d = ((xpos-bg_w/2) * scale) + bg_w/2;
              var y2d = ((ypos) * scale) + adj_y - (zpos*0.01);
              if (y2d > bg_h) y2d = bg_h;
              else if (y2d < 0) y2d = 0;
              else sv = true;
              if (fp) protonFigCTX.moveTo(x2d, y2d);
              else protonFigCTX.lineTo(x2d, y2d);
              fp = false;
            }
            if (sv) protonFigCTX.stroke();
          }
        }
      }
      
      livebg()