function eliminarPelicula(id){
    Swal.fire({
        title:"¿Está seguro de querer eliminar la pelicula?",
        showDenyButton: true,
        confirmButtonText: "Si",
        denyButtonText:"No"
    }).then((result) => {
        if(result.isConfirmed){
            location.href="/eliminarPelicula/" + id
        }
    })
}