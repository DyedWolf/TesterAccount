const apiUrl = 'http://gift.yuanpaikeji.com'; //主域名
const linkUrl = 'http://gift.yuanpaikeji.com/liwu_wap'; //网页域名
// const linkUrl = 'http://192.168.0.66:5501'; //网页域名
// localStorage.setItem('token','');
let token = localStorage.getItem('token') || false;



// ajax function

// ajaxFuction({
//   url: true,
//   data: true,
//   fun(res) {

//   }
// });

function ajaxFuction(DATA) {
  var url = DATA.url || ''; //链接
  var data = DATA.data || {}; //传递的数据
  var msgHide = DATA.msgHide || false; //是否隐藏msg
  var fun = DATA.fun || function () {}; //ajax成功后的回调
  var processData = DATA.processData == 1 ? false : true; //不需要将传输的数据序列化 上传文件的时候用

  data.token = token; //每次走接口都加token

  $.ajax({
    url: url,
    type: 'POST',
    // headers: {
    //   "Access-Control-Allow-Origin": "*",
    //   "Access-Control-Allow-Headers": "Authorization",
    //   "Authorization": '123'
    // },
    xhrFields: {
      withCredentials: true
    },
    crossDomain: true,
    async: false,
    dataType: 'json',
    // contentType: false,
    processData: processData,
    data: data,
    success: function (res) {

      if (res.ReturnStatus == 'SUCCESS') {
        fun(res);
      } else {
        if (!msgHide) {
          if (layer.msg) {
            layer.msg(res.Error.ErrorInfo);
          } else {
            layer.open({
              type: 0,
              skin: 'msg',
              time: 2,
              content: res.Error.ErrorInfo
            });
          }
        }
      }
    }
  });
};

// 对象和数组克隆
function objCopy(res) {
  var resJson = JSON.stringify(res);
  var data = JSON.parse(resJson);
  return data;
};

//滚动到顶部
$('body').on('click', '.gotoTop', function () {
  $('body,html').animate({
    scrollTop: 0
  }, 200);
});


// 窗口滚动
function toScroll(num) {
  if (document.documentElement.scrollTop >= 0) {
    document.documentElement.scrollTop = num;
    return false;
  }

  if (document.body.scrollTop >= 0) {
    document.documentElement.scrollTop = num;
    return false;
  }
}