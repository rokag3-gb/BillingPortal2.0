  /* 입력 자동 Setting */
  function f_init()
  {
      var frm_pay = document.frm_pay;

      var today = new Date();
      var year  = today.getFullYear();
      var month = today.getMonth() + 1;
      var date  = today.getDate();
      var time  = today.getTime();

      if(parseInt(month) < 10)
      {
          month = "0" + month;
      }

      if(parseInt(date) < 10)
      {
          date = "0" + date;
      }


      /*--공통--*/        
      frm_pay.EP_mall_id.value        = "T5102001";                              //가맹점 ID
      frm_pay.EP_mall_nm.value        = "이지페이8.0 모바일";                    //가맹점명
      frm_pay.EP_order_no.value       = "ORDER_" + year + month + date + time;   //가맹점 주문번호    
                                                                                 //결제수단(select)
      frm_pay.EP_currency.value       = "00";                                    //통화코드 : 00-원
      frm_pay.EP_product_nm.value     = "테스트상품";                            //상품명
      frm_pay.EP_product_amt.value    = "51004";                                 //상품금액
                                                                                 //가맹점 return_url(윈도우 타입 선택 시, 분기)
      frm_pay.EP_lang_flag.value      = "KOR"                                    //언어: KOR / ENG
      frm_pay.EP_charset.value        = "EUC-KR"                                 //가맹점 Charset: EUC-KR(default) / UTF-8
      frm_pay.EP_user_id.value        = "psj1988";                               //가맹점 고객 ID
      frm_pay.EP_memb_user_no.value   = "15123485756";                           //가맹점 고객 일련번호
      frm_pay.EP_user_nm.value        = "홍길동";                                //가맹점 고객명
      frm_pay.EP_user_mail.value      = "kildong@kicc.co.kr";                    //가맹점 고객 이메일
      frm_pay.EP_user_phone1.value    = "0221471111";                            //가맹점 고객 번호1
      frm_pay.EP_user_phone2.value    = "01012345679";                           //가맹점 고객 번호2
      frm_pay.EP_user_addr.value      = "서울시 금천구 가산동";                  //가맹점 고객 주소
      frm_pay.EP_product_type.value   = "0";                                     //상품정보구분 : 0-실물, 1-서비스
      frm_pay.EP_product_expr.value   = "";                              //서비스기간 : YYYYMMDD
      frm_pay.EP_return_url.value     = "http://localhost:8000/payment/result";      // Return 받을 URL (HTTP부터 입력)

                                      
      /*--신용카드--*/                    
      frm_pay.EP_usedcard_code.value  = "";                                      //사용가능한 카드 LIST
      frm_pay.EP_quota.value          = "";                                      //할부개월

                                                                                 //무이자 여부(Y/N) (select)   
      frm_pay.EP_noinst_term.value    = "029-02:03";                             //무이자기간
                                                                                 //카드사포인트 사용여부(select) 
      frm_pay.EP_point_card.value     = "029-40";                                //포인트카드 LIST
                                                                                 //조인코드(select)
                                                                                 //국민 앱카드 사용(select)                                                                                  
                                                                                                                 
      /*--가상계좌--*/                   
      var vacct_until = new Date();
      vacct_until.setDate(vacct_until.getDate() + 7);   
      var vmonth =  today.getMonth() + 1
      if(parseInt(month) < 10)
      {
        vmonth = "0" + vmonth;
      }

      var vdate = today.getDate()
      if(parseInt(date) < 10)
      {
        vdate = "0" + vdate;
      } 
      console.log(`${today.getFullYear()}${vmonth}${vdate}`)
      frm_pay.EP_vacct_bank.value     = "";                                      //가상계좌 사용가능한 은행 LIST 
      frm_pay.EP_vacct_end_date.value = `${today.getFullYear()}${vmonth}${vdate}`;    //입금 만료 날짜
      frm_pay.EP_vacct_end_time.value = "153025";                                //입금 만료 시간
      
      

  }

  /* 인증창 호출, 인증 요청 */
  function f_cert()
  {
      var frm_pay = document.frm_pay;
      
      /*  주문정보 확인 */
      if( !frm_pay.EP_order_no.value ) 
      {
          alert("가맹점주문번호를 입력하세요!!");
          frm_pay.EP_order_no.focus();
          return;
      }

      if( !frm_pay.EP_product_amt.value ) 
      {
          alert("상품금액을 입력하세요!!");
          frm_pay.EP_product_amt.focus();
          return;
      } 

      /* UTF-8 사용가맹점의 경우 EP_charset 값 셋팅 필수 */
      if( frm_pay.EP_charset.value == "UTF-8" )
      {
          // 한글이 들어가는 값은 모두 encoding 필수.
          frm_pay.EP_mall_nm.value        = encodeURIComponent( frm_pay.EP_mall_nm.value );
          frm_pay.EP_product_nm.value     = encodeURIComponent( frm_pay.EP_product_nm.value );
          frm_pay.EP_user_nm.value        = encodeURIComponent( frm_pay.EP_user_nm.value );
          frm_pay.EP_user_addr.value      = encodeURIComponent( frm_pay.EP_user_addr.value );
      }


      /* 가맹점에서 원하는 인증창 호출 방법을 선택 */

      if( frm_pay.EP_window_type.value == "iframe" )
      {
          easypay_webpay(frm_pay,"./payment/request","hiddenifr","0","0","iframe",30);

          if( frm_pay.EP_charset.value == "UTF-8" )
          {
              // encoding 된 값은 모두 decoding 필수.
              frm_pay.EP_mall_nm.value        = decodeURIComponent( frm_pay.EP_mall_nm.value );
              frm_pay.EP_product_nm.value     = decodeURIComponent( frm_pay.EP_product_nm.value );
              frm_pay.EP_user_nm.value        = decodeURIComponent( frm_pay.EP_user_nm.value );
              frm_pay.EP_user_addr.value      = decodeURIComponent( frm_pay.EP_user_addr.value );
          }
      }
      else if( frm_pay.EP_window_type.value == "popup" )
      {
          easypay_webpay(frm_pay,"./payment/request","hiddenifr","","","popup",30);

          if( frm_pay.EP_charset.value == "UTF-8" )
          {
              // encoding 된 값은 모두 decoding 필수.
              frm_pay.EP_mall_nm.value        = decodeURIComponent( frm_pay.EP_mall_nm.value );
              frm_pay.EP_product_nm.value     = decodeURIComponent( frm_pay.EP_product_nm.value );
              frm_pay.EP_user_nm.value        = decodeURIComponent( frm_pay.EP_user_nm.value );
              frm_pay.EP_user_addr.value      = decodeURIComponent( frm_pay.EP_user_addr.value );
          }
      }
  }

  function f_submit()
  {
      var frm_pay = document.frm_pay;

      frm_pay.target = "_self";
      frm_pay.action = "../easypay_request.jsp";
      frm_pay.submit();
  }