// PC OR Mobile 
let is_mobile = false;
$(document).ready(function(){
	if($(document).width() < 1025)
		is_mobile = true;

	const swiper_gallery_thumb = new Swiper(".swiper-gallery-thumb", {
		//spaceBetween: 30,
		slidesPerView: 7,
		//freeMode: true,
		centeredSlides: true,
		watchSlidesProgress: true,
		watchSlidesVisibility: true, 
		initialSlide: 3,
		navigation: {
			nextEl: ".thumb-img .swiper-next",
			prevEl: ".thumb-img .swiper-prev",
		},
		breakpoints:{
			320:{
				//spaceBetween: 10,
				slidesPerView: 3,
			},
			1025:{
				//spaceBetween: 20,
				slidesPerView: 5,
			},
			1201:{
				//spaceBetween: 20,
				slidesPerView: 7,
			},
		}
	});

	const swiper_gallery = new Swiper(".swiper-gallery", {
		initialSlide:3,
		spaceBetween: 10,
		thumbs: {
		  swiper: swiper_gallery_thumb,
		},
	});

	 // 썸네일 클릭 시 해당 썸네일을 중앙으로 이동
	 $(".swiper-gallery-thumb .swiper-slide").on("click", function () {
        let index = $(this).index(); // 클릭한 썸네일의 인덱스 값 가져오기
        swiper_gallery_thumb.slideTo(index); // 해당 썸네일로 이동
        swiper_gallery.slideTo(index); // 메인 이미지 슬라이드도 해당 썸네일에 맞춰 이동

		updateThumbnailSize();
    });

    // 썸네일 크기 업데이트 함수
    function updateThumbnailSize() {
        const slides = $(".swiper-gallery-thumb .swiper-slide");
        const activeIndex = swiper_gallery_thumb.activeIndex;

        slides.each(function (index) {
            if (index === activeIndex) {
                $(this).removeClass("small").removeClass("smalls").removeClass("smallss").addClass("active"); // 활성화된 썸네일
            } else if (index === activeIndex - 1 || index === activeIndex + 1) {
                $(this).removeClass("active").removeClass('smalls').removeClass('smallss').addClass("small"); // 양옆 썸네일
			} else if (index === activeIndex - 2 || index === activeIndex + 2) {
                $(this).removeClass("active").removeClass('smallss').addClass("smalls"); // 양옆 썸네일
			} else if (index === activeIndex - 3 || index === activeIndex + 3) {
                $(this).removeClass("active").addClass("smallss"); // 양옆 썸네일
			} else {
                $(this).removeClass("active small"); // 그 외 썸네일
            }
        });
    }

    // 초기 썸네일 크기 설정
    updateThumbnailSize();

	// 전체 선택 체크박스 클릭 시
    $('.check-all').click(function() {
        $('.check-item').prop('checked', this.checked);
    });

    // 개별 체크박스 클릭 시
    $('.check-item').click(function() {
        $('.check-all').prop('checked', $('.check-item:checked').length === $('.check-item').length);
    });
	
	$('.js-btn-menu').on('click',function(){
    	$('header').toggleClass('menu-open');               
   	});

	/* ==============================
	* loading
	==================================*/
	let isMouseDown = false;  // 마우스가 눌렸는지 확인하는 변수
	let transitionId = null;
	
	const mask = document.querySelector('.mask');
	const windowWidth = document.documentElement.clientWidth;
	const windowHeight = document.documentElement.clientHeight;
	
	//반지름 수치가 필요하므로 지름 반으로 나누기
	const maxRadius = Math.sqrt(windowWidth ** 2 + windowHeight ** 2) * 0.5;
	const duration = 1000; // 애니메이션 시간 (1초)
	   
	function easeInOutCubic(t) {
		return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
	}

	function expandMask(){
		running = true;
		startTime = performance.now();

		transitionId = setInterval(() => {
			const now = performance.now();
			let progress = (now - startTime) / duration;
			progress = easeInOutCubic(progress);    //easing 적용
			radius = progress * maxRadius;

			mask.style.setProperty('--mask-radius', `${radius}px`);

			if(progress >= 1){
				clearInterval(transitionId);
			}
		}, 16);//16ms = 60fps
	}

	// 마우스로 ENTER 눌렀을 때
	$('.loading-bar').mousedown(function(event) {
		$(this).addClass('on');
	});

	// 마우스를 떼었을 때
	$(document).mouseup(function() {
		if (isMouseDown)
			isMouseDown = false;  // 마우스 떼기

		$('.loading-bar').removeClass('on');
	});

	setTimeout(function(){// 1. 로딩 다됬을 때 ENTER로 변경되는 부분(지금은 임시로 SetTimeout으로 해둠)
		loading_txt();
	},1000);

	$('.loading-bar').click(function(){ // 2. ENTER 버튼 클릭시
		transitionId == null && loading_down();
	});

	function loading_txt(){// ENTER 글자 애니메이션
		$('.loading-wrap').addClass('on');
	}

	function loading_down(){ // ENTER 버튼이 내려가고, 마스크가 씌워지는 함수
		if($('.loading-wrap').hasClass('on'))
			$('.loading-wrap').addClass('enter');

		setTimeout(function(){ // 하얀 원 약간의 딜레이 주고 보여지게 하기
			$('.mask').show();
			expandMask();
		},800);
	}

	AOS.init()
});