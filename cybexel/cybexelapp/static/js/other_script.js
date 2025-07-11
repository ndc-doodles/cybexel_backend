document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const navbar = document.getElementById('navbar');
  const enquireBtn = document.getElementById('enquire-btn');
  const navLinks = document.querySelectorAll('.nav-link');
  const menuIcon = document.getElementById('menu-icon');
  const logo = document.getElementById('logo');

  // Toggle mobile menu
  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    mobileMenu.classList.toggle('translate-x-full');
    mobileMenu.classList.toggle('translate-x-0');
  });

  // Close menu when clicking outside
  window.addEventListener('click', (e) => {
    if (
      !mobileMenu.contains(e.target) &&
      !toggleBtn.contains(e.target) &&
      !e.target.closest('#menu-icon')
    ) {
      mobileMenu.classList.add('translate-x-full');
      mobileMenu.classList.remove('translate-x-0');
    }
  });

  // Scroll behavior
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('bg-white/30', 'backdrop-blur-md', 'shadow-md', 'text-black');
      navbar.classList.remove('text-white');

      if (enquireBtn) {
        enquireBtn.classList.remove('bg-white', 'text-[#151a37]');
        enquireBtn.classList.add('bg-[#151a37]', 'text-white');
      }

      navLinks.forEach(link => {
        link.classList.remove('text-white');
        link.classList.add('text-black');
      });

      menuIcon.classList.remove('text-white');
      menuIcon.classList.add('text-black');
      logo.src = "/static/images/logo2.png"; // Correct Django static path
    } else {
      navbar.classList.remove('bg-white/30', 'backdrop-blur-md', 'shadow-md', 'text-black');
      navbar.classList.add('text-white');

      if (enquireBtn) {
        enquireBtn.classList.add('bg-white', 'text-[#151a37]');
        enquireBtn.classList.remove('bg-[#151a37]', 'text-white');
      }

      navLinks.forEach(link => {
        link.classList.add('text-white');
        link.classList.remove('text-black');
      });

      menuIcon.classList.add('text-white');
      menuIcon.classList.remove('text-black');
      logo.src = "/static/images/logo1.png"; // Correct Django static path
    }
  });
});



let fabOpen = false;

window.toggleFab = function() {
  fabOpen = !fabOpen;

  const icon = document.getElementById("fabIcon");
  const buttons = [
    document.getElementById("whatsappBtn"),
    document.getElementById("callBtn")
  ];

  icon.classList.toggle("rotate-45");

  buttons.forEach(btn => {
    if (fabOpen) {
      btn.classList.remove("scale-0", "opacity-0", "pointer-events-none");
    } else {
      btn.classList.add("scale-0", "opacity-0");
      btn.classList.add("pointer-events-none");
    }
  });
};


 document.addEventListener("DOMContentLoaded", function () {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("opacity-100", "translate-y-0");
          entry.target.classList.remove("opacity-0", "translate-y-8");
          observer.unobserve(entry.target); // Animate only once
        }
      });
    }, {
      threshold: 0.1
    });

    document.querySelectorAll('.fade-in-on-scroll').forEach(el => observer.observe(el));
  });









  document.addEventListener("DOMContentLoaded", function() {
      const counters = document.querySelectorAll('.counter');
      counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const duration = 2000;
        const steps = 80;
        const increment = target / steps;
        let current = 0;
        let count = 0;

        const update = () => {
          current += increment;
          if (count < steps) {
            counter.innerText = Math.ceil(current);
            count++;
            setTimeout(update, duration / steps);
          } else {
            counter.innerText = target + "+";
          }
        };

        update();
      });
    });





function openDetailsModal(title, label, skills, description, department) {
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalLabel').innerText = label;
    document.getElementById('modalDescription').innerHTML = description;
    document.getElementById('modalDepartment').innerHTML = department;


    // Store department for use in form
    window.selectedDepartment = department;

    const tagsContainer = document.getElementById('modalTags');
    tagsContainer.innerHTML = '';
    if (skills) {
      skills.split(',').forEach(skill => {
        const tag = document.createElement('span');
        tag.textContent = skill.trim();
        tag.className = 'bg-gray-100 text-xs px-2 py-1 rounded';
        tagsContainer.appendChild(tag);
      });
    }

    document.getElementById('jobModal').classList.remove('hidden');
  }

  function closeModal() {
    document.getElementById('jobModal').classList.add('hidden');
  }

  function closeForm() {
    document.getElementById('formModal').classList.add('hidden');
  }

  function openForm() {
    document.getElementById('jobModal').classList.add('hidden');
    document.getElementById('formModal').classList.remove('hidden');

    document.getElementById('formPosition').value = document.getElementById('modalTitle').textContent;
    document.getElementById('formLabel').value = document.getElementById('modalLabel').textContent;
    document.getElementById('formDepartment').value = document.getElementById('modalDepartment').textContent;
}


  function checkBackdropClose(event) {
    if (event.target.id === 'jobModal') {
      closeModal();
    }
  }


setTimeout(() => {
  const modal = document.getElementById('successModal');
  if (modal) {
    modal.classList.add('hidden');
  }
}, 3000);




//  blog

const blogData = document.getElementById("blogData");

if (blogData) {
  const blogs = JSON.parse(blogData.dataset.blogs);

  document.querySelectorAll(".open-modal-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const index = this.dataset.index;
      openBlogModal(parseInt(index));
    });
  });

  function openBlogModal(index) {
    const blog = blogs[index];
    document.getElementById("modalTitle").innerText = blog.title;
    document.getElementById("modalDate").innerText = blog.date;
    document.getElementById("modalImage").src = blog.image;
    document.getElementById("modalContent").innerHTML = blog.content;
    document.getElementById("blogModal").classList.remove("hidden");
  }

  function closeBlogModal() {
    document.getElementById("blogModal").classList.add("hidden");
  }
}









  
  
 document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  const closeModal = document.getElementById('closeModal');
  const prevButton = document.getElementById('prevImage');
  const nextButton = document.getElementById('nextImage');

  const images = Array.from(document.querySelectorAll('.event-image'));
  let currentIndex = 0;

  // Click on image to open modal
  images.forEach((img, index) => {
    img.dataset.index = index;
    img.addEventListener('click', () => {
      currentIndex = index;
      modalImage.src = img.src;
      modal.classList.remove('hidden');
    });
  });

  // Close modal
  closeModal.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  // Click outside image to close
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });

  // Navigate to previous image
  prevButton.addEventListener('click', (e) => {
    e.stopPropagation();
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    modalImage.src = images[currentIndex].src;
  });

  // Navigate to next image
  nextButton.addEventListener('click', (e) => {
    e.stopPropagation();
    currentIndex = (currentIndex + 1) % images.length;
    modalImage.src = images[currentIndex].src;
  });
});






// alert on job form






 document.addEventListener("DOMContentLoaded", function () {
    const resumeInput = document.getElementById("resumeInput");
    const fileError = document.getElementById("fileError");

    resumeInput.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const fileName = file.name.toLowerCase();
        const fileType = file.type;

        // Validate file extension and MIME type
        if (!fileName.endsWith(".pdf") || fileType !== "application/pdf") {
          fileError.classList.remove("hidden");
          this.value = ""; // Clear invalid file
        } else {
          fileError.classList.add("hidden"); // Hide error
        }
      }
    });
  });