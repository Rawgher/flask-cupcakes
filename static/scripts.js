function cupcakeHTML(cupcake) {
    return `
    <li class="list-group-item" data-cupcake-id=${cupcake.id}>
        <span>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}</span>
        <img src=${cupcake.image} class='cc-image'>
        <button class='btn btn-danger delete-btn'>X</button>
    </li>
    `;
};

async function showAllCupcakes() {
    const res = await axios.get('/api/cupcakes');
    for (let ccData of res.data.cupcakes) {
        let newCC = cupcakeHTML(ccData);
        $('#cupcake-list').append(newCC)
    }
};

$('#new-cc-form').on("submit", async function(e) {
    e.preventDefault();

    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();

    const newCCRes = await axios.post('/api/cupcakes', {
        flavor, size, rating, image
    });

    let newCC = cupcakeHTML(newCCRes.data.cupcake)
    $('#cupcake-list').append(newCC)
    $('#new-cc-form').trigger('reset')
});

$('#cupcake-list').on('click', '.delete-btn', async function(e) {
    e.preventDefault();

    let thisCC = $(e.target).closest('li');
    let ccID = thisCC.attr('data-cupcake-id');

    await axios.delete(`/api/cupcakes/${ccID}`);
    thisCC.remove();
})


showAllCupcakes();