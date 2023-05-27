const endrideEl = document.querySelector('.end-ride-btn');
const reviewEl = document.querySelector('.review-wrapper');
const closeBtn = document.querySelector('.close-review ');
const lcloseBtn = document.querySelector('.l-close-review');
const creviewBtn = document.querySelector('.c-review-btn');
const lreviewBtn = document.querySelectorAll('.l-review-btn');
const lreviewEl = document.querySelector('.l-review-wrapper');
const stars = document.querySelectorAll('.rating-star');
const stars2 = document.querySelectorAll('.rating-star-2');
const rating = document.querySelector('#id_rating');
const rating2 = document.querySelector('#id_rating_2')
let ride_id, user_id, ride;

if (endrideEl) {
	endrideEl.addEventListener('click', (e) => {
		e.preventDefault();
		reviewEl.style.display = 'flex';
	});
}

closeBtn.addEventListener('click', (e) => {
	e.preventDefault();
	reviewEl.style.display = "none";
});

lcloseBtn.addEventListener('click', (e) => {
	e.preventDefault();
	lreviewEl.style.display = "none";
});

lreviewBtn.forEach((element) => {
	element.addEventListener('click', (e) => {
		e.preventDefault();
		user_id = e.target.getAttribute('data-user-id');
		ride_id = e.target.getAttribute('data-ride-id');
		ride = e.target.getAttribute('data-user-ride-id');
		lreviewEl.style.display = 'flex';
	});
});

creviewBtn.addEventListener('click', (e) => {
	e.preventDefault();
	review = document.querySelector('.review-text').value;
	fetch("/api/v1/review/create//", {
		method: "POST",
		body: JSON.stringify({
			review: review,
			user_id: user_id,
			ride_id: ride_id,
			rating: rating2.value
		})
	})
	.then(res => {
		if (!res.ok) {
			throw new Error("Could not create review");
		} 
		return res.json()
	})
	.then(data => {
		window.location = `/ride-detail/${ride}`;
	})
	.catch(error => console.log(error))
});

stars.forEach((star, index) => {
	star.addEventListener('click', () => {
		rating.value = index + 1;
		stars.forEach((s, i) => {
			if (i <= index ) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
	
	star.addEventListener('mouseover', () => {
		stars.forEach((s, i) => {
			if (i <= index) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
	
	star.addEventListener('mouseout', () => {
		stars.forEach((s, i) => {
			if (i <= index) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
})

stars2.forEach((star, index) => {
	star.addEventListener('click', () => {
		rating2.value = index + 1;
		stars2.forEach((s, i) => {
			if (i <= index ) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
	
	star.addEventListener('mouseover', () => {
		stars2.forEach((s, i) => {
			if (i <= index) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
	
	star.addEventListener('mouseout', () => {
		stars2.forEach((s, i) => {
			if (i <= index) {
				s.classList.add('gold');
			} else {
				s.classList.remove('gold');
			}
		});
	});
})
