/*
 *Progcessed By JSDec in 0.00s
 *JSDec - JSDec.js.org
 */
$(function () {
  var preArr = {},
    imgsKeyArr = [],
    imgDetailArr = [],
    images = {},
    RAM = 0; //preArr:页面上显示json字符传，imgsKeyArr:观看图片时，图片的名称images:base64图片，RAM：所占内存
  // 播放svga
  var player = new SVGA.Player('#demoCanvas');
  var parser = new SVGA.Parser('#demoCanvas'); // Must Provide same selector eg:#demoCanvas IF support IE6+


  function playSvga(file) {
    //初始化数据
    preArr = {};
    imgsKeyArr = [];
    imgDetailArr = [];
    images = {};
    RAM = 0;
    // $('.animate-detail-list').html('<li>内存占用：<span class="memory">0 M</span></li>')
    // $('.preview-img').css('background-image','url()')
    $('.myImgs').attr('src', '')
    $('.svga-memory').text(0 + 'M')
    //实现效果
    $('.null-svga').hide();
    $('.drag-box').show();
    $('.kong-title').hide();
    $('.preview-pre').show();
    $('.kong-text').hide();
    $('.svga-detail').show();
    $('.choose').show();
    parser.load(file, function (videoItem) {
      console.log(videoItem)
      player.loops = 0;
      player.clearsAfterStop = false;
      player.setVideoItem(videoItem);
      player.startAnimation();


      // 自适应礼物框
      //  修改礼物显示框大小 通过宽度比例计算
      var svgaSize = videoItem.videoSize; //视频的大小
      var wwwww = 375;
      var bili = svgaSize.width / wwwww; //宽高比例
      $('#demoCanvas').width(wwwww + 'px');
      $('#demoCanvas').height(svgaSize.height / bili + 'px');
      $('.content .phone-box').css('background', 'none');
      $('.phone-box').css({
        'widht': 'auto',
        'height': 'auto'
      });

      // svga动画页面上显示的大小
      images = videoItem.images;
      //观看图片
      for (var item in videoItem.images) {
        imgsKeyArr.push(item)
      }
      if (imgsKeyArr.length > 0) {
        $('.myImgs').attr('src', 'data:image/png;base64,' + images[imgsKeyArr[0]])
        // $('.preview-img').css('background-image','url()')
      }

      // json字符串
      preArr.version = videoItem.version;
      preArr.FPS = videoItem.FPS;
      preArr.frames = videoItem.frames;
      preArr.videoSize = videoItem.videoSize;
      $('.preview-pre').html(syntaxHighlight(preArr))
      // console.log(imgsKeyArr.length)


      $('.animate-time').text((videoItem.frames / videoItem.FPS).toFixed(2) + 's')

      if (imgsKeyArr.length == 1) {
        getImgSize(videoItem.sprites[0], imgsKeyArr, images, true)
      } else if (imgsKeyArr.length > 0) {
        getImgSize(videoItem.sprites, imgsKeyArr, images, false)
      }

    })

  }

  function getImgSize(size, names, images, isonly) {
    // console.log(images)
    // isonly:是否单张图片
    var str = ''
    if (!isonly) {
      imgDetailArr = quchong(size);
      // 排序 imgDetailArr
      imgDetailArr.sort((prev, next) => {
        return names.indexOf(prev.imageKey) - names.indexOf(next.imageKey)
      })
      // console.log(imgDetailArr)
      for (var i = 0; i < imgDetailArr.length; i++) {
        var activeClass = 'detail-item common-pad-t-min'
        if (i == 0) {
          activeClass += ' is-active'
        }
        var n = getImageSizeFromBase64Data(images[imgDetailArr[i].imageKey]);
        RAM += n.width * n.height * 4;
        str += '<li class="' + activeClass + '">' + imgDetailArr[i].imageKey + ' --- {"width":' + n.width + ',"height":' + n.height + '}</li>'
      }
    } else {
      imgDetailArr.push(size);
      var imgKey = ''
      for (var key in images) {
        imgKey = key
      }
      var n = getImageSizeFromBase64Data(images[imgKey]);
      RAM += n.width * n.height * 4;
      str += '<li class="is-active">' + imgDetailArr[0].imageKey + ' --- {"width":' + n.width + ',"height":' + n.height + '}</li>'

    }
    $('.animate-detail-list').html(str)
    // console.log(Math.round(RAM/1048576 * 100)/100+ 'M')
    $('.memory').text(Math.round(RAM / 1048576 * 100) / 100 + 'M')
    // $('.svga-memory').text(Math.round(RAM/1048576 * 100)/100+ 'M')
  }

  // 计算内存
  function getImageSizeFromBase64Data(e) {
    if (e) {
      var t = convertDataURIToBinary(e),
        r = 256 * t[18] + t[19],
        o = 256 * t[22] + t[23];
      return {
        width: r,
        height: o
      }
    }

  }

  function convertDataURIToBinary(e) {
    var t = window.atob(e),
      r = t.length,
      o = new Uint8Array(new ArrayBuffer(r));
    for (i = 0; i < r; i++)
      o[i] = t.charCodeAt(i);
    return o
  }

  //点击预览图片
  $('.animate-detail-list').on('click', '.detail-item', function () {
    $(this).addClass('is-active').siblings().removeClass('is-active')
    $('.myImgs').attr('src', 'data:image/png;base64,' + images[imgsKeyArr[$(this).index()]])
    // $('.preview-img').css('background-image','url(data:image/png;base64,'+images[imgsKeyArr[$(this).index()-1]]+')')
  })

  //数组去重
  function quchong(arr1) {
    const res = new Map();
    return arr1.filter((a) => !res.has(a.imageKey) && res.set(a.imageKey, 1))
  }

  //json字符串转换成页面上看到的效果
  function syntaxHighlight(json) {
    if (typeof json != 'string') {
      json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
      return '<span>' + match + '</span>';
    });
  }

  //点击按钮预览
  // function onFileChangeHandle(event) {
  //     console.log(event[0].size)
  //     $('.svga-size').text(Math.round(event[0].size/1048576*100)/100+ 'M')
  //     const file = window.URL.createObjectURL(event[0]);
  //     playSvga(file)
  // }
  // 拖拽预览
  var drag = document.getElementById('drag')
  drag.ondragenter = function (event) {
    event.preventDefault()
  }
  drag.ondragover = function (event) {
    event.preventDefault()
  }
  drag.ondrop = function (event) {
    var fileName = event.dataTransfer.files[0].name;
    var fileType = fileName.substr(fileName.lastIndexOf(".")).toUpperCase();
    // console.log(fileType)
    if (fileType != '.SVGA') {
      alert('请使用svga格式的文件')
      return false;
    }
    
    var formData=new FormData();
    formData.append("file",event.dataTransfer.files[0]);

    // 推荐礼物列表
    ajaxFuction({
      url: apiUrl + "/api/Svgabrowse/browse_file",
      data: formData,
      processData:1,
      fun: function (res) {
        //   console.log(res)
      }
    });


    $('.svga-size').text(Math.round(event.dataTransfer.files[0].size / 1048576 * 100) / 100 + 'M')
    event.preventDefault()
    const file = window.URL.createObjectURL(event.dataTransfer.files[0]);
    playSvga(file)
    var uploadFiles = event.dataTransfer.files[0]
    // console.log(file)
    console.log(file)
    console.log(uploadFiles)
    uploadFile(uploadFiles)
  }
  var drag2 = document.getElementById('demoCanvas')
  drag2.ondragenter = function (event) {
    event.preventDefault()
  }
  drag2.ondragover = function (event) {
    event.preventDefault()
  }
  drag2.ondrop = function (event) {
    var fileName = event.dataTransfer.files[0].name;
    var fileType = fileName.substr(fileName.lastIndexOf(".")).toUpperCase();
    // console.log(fileType)
    if (fileType != '.SVGA') {
      alert('请上传svga格式的文件')
      return false;
    }
    
    var formData=new FormData();
    formData.append("file",event.dataTransfer.files[0]);

    // 推荐礼物列表
    ajaxFuction({
      url: apiUrl + "/api/Svgabrowse/browse_file",
      data: formData,
      processData:1,
      fun: function (res) {
        //   console.log(res)
      }
    });
    
    $('.svga-size').text(Math.round(event.dataTransfer.files[0].size / 1048576 * 100) / 100 + 'M')
    event.preventDefault()
    const file = window.URL.createObjectURL(event.dataTransfer.files[0]);
    playSvga(file)
    var uploadFiles = event.dataTransfer.files[0]
    // console.log(file)
    console.log(file)
    console.log(uploadFiles)
    uploadFile(uploadFiles)

  }

  // 上传文件
  function uploadFile(obj) {
    //   var data = new FormData();
    //   data.append('file', obj);
    //   $.ajax({
    //     method: 'post',
    //     url: 'http://svga.8zuu.com/index/index/mmmfty',
    //     data: data,
    //     processData: false,
    //     // 告诉jQuery不要去设置Content-Type请求头
    //     contentType: false,
    //     success(res) {
    //       console.log(res)
    //     },
    //     error(error) {
    //       console.log(error)
    //     }
    //   })
  }

  // 预览svga背景颜色
  const colorArr = ['#000000', '#FFFFFF', '#398EFF', '#14B446', '#F9D02F', '#FD415A']
  $('.choose-color').on('click', function () {
    var currentIndex = $(this).index()
    $('.phone').css('backgroundColor', colorArr[currentIndex])
  });
  // 手机预览切换
  $('.phone-item').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    var myWidth = $(this).attr('_setWidth')
    var myHeight = $(this).attr('_setHeight')
    $('.phont-size').text('手机分辨率' + myWidth + 'x' + myHeight + '')
    var size = 667 / myHeight;
    // console.log(size,myWidth*size)
    $('.phone-box').css({
      width: myWidth * size + 'px',
      height: 667 + 'px'
    })
    if (imgsKeyArr.length > 0) {
      player.startAnimation(false)
    }
  })
  // 模式切换
  $('.mode-item').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    player.setContentMode($(this).attr('_setMode'));
    player.startAnimation(false)
  })
})