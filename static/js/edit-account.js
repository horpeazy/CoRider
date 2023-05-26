const profileImage = document.querySelector('.profile-picture');
const imageInput = document.querySelector('#id_profile_picture');

imageInput.addEventListener('change', () => {
	const file = imageInput.files[0];
	const fileUrl = URL.createObjectURL(file);
	profileImage.src = fileUrl;
})
