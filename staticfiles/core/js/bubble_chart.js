function initBubbleChart(data, fecha) {
    const container = document.getElementById('bubble-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    const color = d3.scaleOrdinal(d3.schemeTableau10); 

    // Preparamos los datos
    const root = d3.hierarchy(data).sum(d => d.value);

    // CALCULA EL RADIO AQUÍ:
    // Usamos una escala para que los valores de BigQuery se conviertan a un radio visible en píxeles
    const maxRadius = width * 0.05; // Las burbujas grandes ocuparán el 15% del ancho de pantalla
    const minRadius = width * 0.001; // Las burbujas pequeñas ocuparán el 2%

    const radiusScale = d3.scaleSqrt()
    .domain([0, d3.max(root.leaves(), d => d.value)])
    .range([minRadius, maxRadius]);    


    root.leaves().forEach(d => {
    d.r = radiusScale(d.value); // Asignamos el radio calculado
    });

    const svg = d3.select("#bubble-container")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`) // ¡Esto es el secreto de la responsividad!
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("width", "100%")
        .attr("height", "100%");

    // Creamos los nodos
    const node = svg.selectAll("g")
        .data(root.leaves())
        .enter().append("g");

    // Dibujamos círculos
    node.append("circle")
    .attr("r", d => d.r)
    .attr("fill", (d, i) => color(i))
    .attr("stroke", "#fff")
    .style("cursor", "pointer") // Cambia el puntero al pasar sobre la bola
    .on("click", (event, d) => {
        // Opción A: Redirigir a una página de noticias filtrada
        const slug = d.data.name.toLowerCase().replace(/\s+/g, '-');
        window.location.href = `/noticias/${slug}/${fecha}`;
        
        // Opción B: Si tienes un modal, podrías llamar a una función aquí:
        // abrirModalNoticias(d.data.name);
    });


    // Agregamos texto
    node.append("text")
        .attr("dy", ".3em")
        .style("text-anchor", "middle")
        .text(d => d.data.name)
        .style("font-size", "12px")
        .style("fill", "#000");


        // Antes de iniciar la simulación, dales posiciones aleatorias dentro del canvas
    root.leaves().forEach(d => {
        d.x = Math.random() * width;
        d.y = Math.random() * height;
    });

    // LA SIMULACIÓN DE FUERZAS
    d3.forceSimulation(root.leaves())
        .force("charge", d3.forceManyBody().strength(15)) // Repulsión entre burbujas
        .force("center", d3.forceCenter(width / 2, height / 2)) // Gravedad hacia el centro
        .force("collision", d3.forceCollide().radius(d => d.r + (width * 0.005))) // Evita solapamiento
        // ESTO MANTIENE EL MOVIMIENTO CONSTANTE:
        .alphaDecay(0) 
        .alphaTarget(0.01)
        .on("tick", () => {
            // Actualizamos la posición en cada frame
            node.attr("transform", d => `translate(${d.x}, ${d.y})`);
        });

    node.selectAll("circle")
    .on("mouseover", function() {
        d3.select(this).attr("stroke", "#000").attr("stroke-width", 2);
    })
    .on("mouseout", function() {
        d3.select(this).attr("stroke", "#fff").attr("stroke-width", 1);
    });
}