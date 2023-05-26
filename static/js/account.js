const accountWrapper = document.querySelector('.account-wrapper');
const accountDetail = document.querySelector('.account-detail');
const personalCard = document.querySelector('.personal-card');
const vehicleCard = document.querySelector('.vehicle-card');
const accountInfo = document.querySelector('.account-info');
const vehicleInfo = document.querySelector('.vehicle-info');
const backEl = document.querySelector('.back');

personalCard.addEventListener('click', () => {
	vehicleInfo.style.display = 'none';
	accountInfo.style.display = 'block';
	accountWrapper.style.left = '-100%';
	accountDetail.style.left = '0';
	
})

vehicleCard.addEventListener('click', () => {
	accountInfo.style.display = 'none';
	vehicleInfo.style.display = 'block';	
	accountWrapper.style.left = '-100%';
	accountDetail.style.left = '0';
})

backEl.addEventListener('click', () => {
	accountWrapper.style.left = '0';
	accountDetail.style.left = '100%';
})
