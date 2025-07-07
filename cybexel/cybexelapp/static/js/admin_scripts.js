function addSkillField() {
    const container = document.getElementById('skillsContainer');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'skills[]';
    input.placeholder = 'Enter a skill';
    input.className = 'w-full p-2 border border-gray-300 rounded';
    container.appendChild(input);
  }




  function editStat(id, title, count) {
    // Set values in the modal
    document.getElementById('statId').value = id;
    document.getElementById('statCount').value = count;
    document.getElementById('modal-title').innerText = title;

    // Show modal
    const modal = document.getElementById('editModal');
    modal.classList.remove('hidden');
    modal.classList.add('flex'); // Make sure flex is in modal's class list
  }

  function closeModal() {
    const modal = document.getElementById('editModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }

  function saveStat(formElement) {
  const id = document.getElementById('statId').value;
  const count = document.getElementById('statCount').value;
  const url = formElement.getAttribute('data-url');

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `id=${encodeURIComponent(id)}&count=${encodeURIComponent(count)}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      document.getElementById('stat-count-' + id).innerText = data.new_count;
      closeModal();
    }
  })
  .catch(error => {
    console.error("Fetch error:", error);
  });

  return false;
}






