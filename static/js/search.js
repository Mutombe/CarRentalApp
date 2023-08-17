$(document).ready(function() {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResultsContainer");

    searchInput.addEventListener("input", function() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm.length > 0) {
            $.ajax({
                url: "/search_cars/",
                type: "GET",
                data: { search: searchTerm },
                success: function(response) {
                    const results = response;

                    searchResults.innerHTML = "";

                    if (results.length > 0) {
                        results.forEach(function(car) {
                            searchResults.innerHTML += `
                                <div class="card">
                                    <div class="card-body" data-mdb-perfect-scrollbar="true" style="position: relative; height: 100px">
                                  
                                        <table class="table mb-0">
                                            <tbody>
                                                <tr class="fw-normal">
                                                <th>
                                                    <img src="${car.image}"
                                                    class="shadow-1-strong rounded-circle" alt="avatar 1"
                                                    style="width: 55px; height: auto;">
                                                    <span class="ms-2">${car.make}</span>
                                                </th>
                                                <td class="align-middle">
                                                    <span>${car.car_model}</span>
                                                </td>
                                                <td class="align-middle">
                        
                                                    <a href="{% url 'car_list' %}"><h6 class="mb-0"><span class="badge bg-danger">View</span></h6></a>
                                                </td>
                                                <td class="align-middle">
                                                    <a href="#!" data-mdb-toggle="tooltip" title="Book"><i
                                                        class="fas fa-check text-success me-3"></i></a>
                                                {% if car.is_booked %}
                                                    <a href="#!" data-mdb-toggle="tooltip" title="Remove"><i
                                                        class="fas fa-trash-alt text-danger"></i>Booked</a>
                                                {% else %} 
                                                    <a href="#!" data-mdb-toggle="tooltip" class="status" title="Rental Status"></i>Available</a>
                                                {% endif %}
                                                </td>
                                                  </tr>
                                
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                        `
                        });
                    } else {
                        const noResultsElement = document.createElement("div");
                        noResultsElement.textContent = "No car found...";
                        searchResults.appendChild(noResultsElement);
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        } else {
            searchResults.innerHTML = "";
        }
    });
});
