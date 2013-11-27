root = exports ? this

icons = 
  tel: "\uf095"
  cnv: "\uf074"
  scr: "\uf108"
  wif: "\uf143"
  vid: "\uf03d"
  ups: "\uf109"
  tv: "\uf02f"
  swt: "\uf0e8"
  prn: "\uf02f"
  pcs: "\uf109"
  mdm: "\uf0ec"
  

      
Network = () ->
  # variables we want to access
  # in multiple places of Network
  width = 600
  height = 600
  # allData will store the unfiltered data
  allData = []
  curLinksData = []
  curNodesData = []
  linkedByIndex = {}
  linkedNodes = {}
  # these will hold the svg groups for
  # accessing the nodes and links display
  nodesG = null
  linksG = null
  # these will point to the circles and lines
  # of the nodes and links
  node = null
  link = null
  # variables to refect the current settings
  # of the visualization
  layout = "force"
  filter = "all"
  sort = "songs"
  # groupCenters will store our radial layout for
  # the group by artist layout.
  groupCenters = null

  # our force directed layout
  force = d3.layout.force()
  # color function used to color nodes
  nodeColors = d3.scale.category20()
  
  tooltip = Tooltip("vis-tooltip", 230)

  network = (selection) ->
    # main implementation
    allData = setupData()
    # create our svg and groups
    vis = d3.select(selection).append("svg")
      .attr("width", width)
      .attr("height", height)
    linksG = vis.append("g").attr("id", "links")
    nodesG = vis.append("g").attr("id", "nodes")
    
    # setup the size of the force environment
    force.size([width, height])

    setLayout("force")
    setFilter("all")
    
    # perform rendering and start force layout
    update()
    
  # The update() function performs the bulk of the
  # work to setup our visualization based on the
  # current layout/sort/filter.
  #
  # update() is called everytime a parameter changes
  # and the network needs to be reset.
  update = () ->
    # filter data to show based on current filter settings.
    curNodesData = filterNodes(allData.nodes)
    curLinksData = filterLinks(allData.links, curNodesData)

    # sort nodes based on current sort and update centers for
    # radial layout
    if layout == "radial"
      artists = sortedArtists(curNodesData, curLinksData)
      updateCenters(artists)

    # reset nodes in force layout
    force.nodes(curNodesData)

    # enter / exit for nodes
    updateNodes()
    # always show links in force layout
    if layout == "force"
      force.links(curLinksData)
      updateLinks()
    else
      # reset links so they do not interfere with
      # other layouts. updateLinks() will be called when
      # force is done animating.
      force.links([])
      # if present, remove them from svg 
      if link
        link.data([]).exit().remove()
        link = null

    # start me up!
    force.start()

  # Public function to switch between layouts
  network.toggleLayout = (newLayout) ->
    force.stop()
    setLayout(newLayout)
    update()
    
    
  # called once to clean up raw data and switch links to
  # point to node instances
  # Returns modified data
  setupData = () ->
    # id's -> node objects
    nodesMap  = mapNodes(nodes) 
    
    #helper function to incerase node conections
    calcuateNodeConections = (nodesMap, n_pk) ->
      if n_pk of linkedNodes
        linkedNodes[n_pk].nr_connections = linkedNodes[n_pk].nr_connections + 1
      else
        n = nodesMap.get(n_pk)
        n.nr_connections = 1
        linkedNodes[n_pk] = n

    connections.forEach (l) ->
      l.source = nodesMap.get(l.fields.device_1)
      l.target = nodesMap.get(l.fields.device_2)
      
      # linkedByIndex is used for link sorting
      linkedByIndex["#{l.source.pk},#{l.target.pk}"] = 1
      
      calcuateNodeConections(nodesMap, l.fields.device_1)
      calcuateNodeConections(nodesMap, l.fields.device_2)
    
    activeNodes = []
    for k, n of linkedNodes
      activeNodes.push(n)
      
    # initialize circle radius scale
    countExtent = d3.extent(activeNodes, (d) -> d.nr_connections)
    circleRadius = d3.scale.sqrt().range([15, 22]).domain(countExtent)
    
    
    activeNodes.forEach (n) ->
      # set initial x/y to values within the width/height
      # of the visualization
      n.x = randomnumber=Math.floor(Math.random()*width)
      n.y = randomnumber=Math.floor(Math.random()*height)
      # add radius to the node so we can use it later
      n.radius = circleRadius(n.nr_connections)   

    
    data = {}
    data["nodes"] = activeNodes
    data["links"] = connections
    data

# Public function to mark nodes
  network.markNodes = (mark) ->
    node.remove()
    updateNodes(mark)

  # switches force to new layout parameters
  setLayout = (newLayout) ->
    layout = newLayout
    if layout == "force"
      force.on("tick", forceTick)
        .charge(-200)
        .linkDistance(50)
    else if layout == "radial"
      force.on("tick", radialTick)
        .charge(charge)
        
  # Helper function to map node id's to node objects.
  # Returns d3.map of ids -> nodes
  mapNodes = (nodes) ->
    nodesMap = d3.map()
    nodes.forEach (n) ->
      nodesMap.set(n.pk, n)
    nodesMap


  # Removes nodes from input array
  # based on current filter setting.
  # Returns array of nodes
  filterNodes = (allNodes) ->
    filteredNodes = allNodes
    if filter == "popular" or filter == "obscure"
      playcounts = allNodes.map((d) -> d.playcount).sort(d3.ascending)
      cutoff = d3.quantile(playcounts, 0.5)
      filteredNodes = allNodes.filter (n) ->
        if filter == "popular"
          n.playcount > cutoff
        else if filter == "obscure"
          n.playcount <= cutoff

    filteredNodes
    
    
  # Removes links from allLinks whose
  # source or target is not present in curNodes
  # Returns array of links
  filterLinks = (allLinks, curNodes) ->
    curNodes = mapNodes(curNodes)
    allLinks.filter (l) ->
      curNodes.get(l.source.pk) and curNodes.get(l.target.pk)
      

  # switches filter option to new filter
  setFilter = (newFilter) ->
    filter = newFilter
    
  # Given two nodes a and b, returns true if
  # there is a link between them.
  # Uses linkedByIndex initialized in setupData
  neighboring = (a, b) ->
    linkedByIndex[a.pk + "," + b.pk] or
      linkedByIndex[b.pk + "," + a.pk]
      
      
  # tick function for force directed layout
  forceTick = (e) ->
    node
      #.attr("cx", (d) -> d.x)
      #.attr("cy", (d) -> d.y)
      .attr("transform", (d) -> "translate(" + d.x + "," + d.y + ")")

    link
      .attr("x1", (d) -> d.source.x)
      .attr("y1", (d) -> d.source.y)
      .attr("x2", (d) -> d.target.x)
      .attr("y2", (d) -> d.target.y)

  # tick function for radial layout
  radialTick = (e) ->
    node.each(moveToRadialLayout(e.alpha))

    node
      .attr("cx", (d) -> d.x)
      .attr("cy", (d) -> d.y)

    if e.alpha < 0.03
      force.stop()
      updateLinks()


  # enter/exit display for nodes
  updateNodes = (mark = "location") ->
    node = nodesG.selectAll(".node")
      .data(curNodesData, (d) -> d.pk)
    
    node.enter().append("g")
      .attr("class", "node")
      .attr("transform", (d) -> "translate(" + d.x + "," + d.y + ")")
      .call(force.drag)
    
    if mark == 2
      setColor = d.location
      
    node.append("circle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", (d) -> d.radius)
      .attr("fill", (d) -> nodeColors(d[mark]))
      #.attr("stroke", (d) -> strokeFor(d))
      #.attr("stroke-width", 1.0)
    
    node.append('text')
      .attr("class", "icon")
      .attr('font-family', 'FontAwesome')
      .attr('font-size', '1em' )
      .attr('fill', 'white' )
      .attr('y', 6 )
      .attr('x', -9 )
      .text((d) -> iconFor(d.item_class__slug) )
      
    #node.append("text")
    #   .attr("class", "nodetext")
    #   .attr('font-size', '.8em' )
    #   .attr('fill', '#666' )
    #   .text((d) -> d.item_template )
       
    node.on("mouseover", showDetails)
      .on("mouseout", hideDetails)
      
    node.on("click", showNodeDetails)

    node.exit().remove()

  # enter/exit display for links
  updateLinks = () ->
    link = linksG.selectAll("line.link")
      .data(curLinksData, (d) -> "#{d.source.pk}_#{d.target.pk}")
    link.enter().append("line")
      .attr("class", "link")
      .attr("stroke", (d) -> nodeColors(d.fields.concetion_type))
      .attr("stroke-opacity", 0.9)
      .attr("x1", (d) -> d.source.x)
      .attr("y1", (d) -> d.source.y)
      .attr("x2", (d) -> d.target.x)
      .attr("y2", (d) -> d.target.y)
      .style("stroke-width", "3px") 
      # .style("stroke-dasharray", (d) ->  if d.fields.concetion_type == 2 than "3, 3")  # <== This line here!!

    link.exit().remove()
  
  # click node
  showNodeDetails = (d,i) ->
    # get detailed data
    $.getJSON "/assets/json/" + d.sku + "/", (data) ->
       properties = data[0].properties
       content = "<h5>other properties</h5><ul>"
       for k, v of properties
          if v != ""
            content += '<li>' + k + ": " + v + '</li>'
       content += "</ul>"  
       $("#properties").html(content)
       
    content = '<h3><a href="/assets/' + d.sku + '/" traget="_blank">' + d.item_template + '</a>'
    content += ' <a class="tiny.button" href="/assets/edit/' + d.sku + '/">edit</a></h3'
    content += '><ul><li>SKU: ' + d.sku + '</li>'
    content += '<li>active: ' + d.active + '</li>'
    content += '<li>state: ' + d.state_name + '</li>'
    content += '<li>owner: ' + d.owner__first_name + " " + d.owner__last_name + '</li>'
    content += '<li>location: ' + d.location__name + '</li>'
    if d.position != undefined
       content += '<li>position: ' + d.position + '</li>'
    if d.function != ""
       content += '<li>function: ' + d.function + '</li>'
    content += '</ul>'
    if d.description != null
       content += '<p>' + d.description  + '</p>'
    if d.users
       content += '<h5>users</h5><ul>'
       for u in d.users
          content += '<li>' + u[1] + ' ' + u[2] + '</li>'
       content += '</ul>'
       
    $("#info").html(content)

    nodesG.selectAll(".node circle").style("stroke-width", 0)
    d3.select(this.firstChild).style("stroke","black")
       .style("stroke-width", 3.0)
    
  
  # Mouseover tooltip function
  showDetails = (d,i) ->
    content = '<p class="main">' + d.item_template + '</span></p>'
    content += '<hr class="tooltip-hr">'
    content += '<p class="main">SKU: ' + d.sku + '</span></p>'
    content += '<p class="main">active: ' + d.active + '</span></p>'
    content += '<p class="main">owner: ' + d.owner__first_name + " " + d.owner__last_name + '</span></p>'
    content += '<p class="main">location: ' + d.location__name + '</span></p>'

    tooltip.showTooltip(content,d3.event)

    # higlight connected links
    if link
      link.attr("stroke-opacity", (l) ->
          if l.source == d or l.target == d then 1.0 else 0.5
      )

      # link.each (l) ->
      #   if l.source == d or l.target == d
      #     d3.select(this).attr("stroke", "#555")

    # highlight neighboring nodes
    # watch out - don't mess with node if search is currently matching
    #node.style("stroke", (n) ->
    #  if (n.searched or neighboring(d, n)) then "#555" else strokeFor(n))
    #  .style("stroke-width", (n) ->
    #    if (n.searched or neighboring(d, n)) then 2.0 else 1.0)
  
    # highlight the node being moused over
    #d3.select(this).style("stroke","black")
    #  .style("stroke-width", 2.0)

  # Mouseout function
  hideDetails = (d,i) ->
    tooltip.hideTooltip()
    # watch out - don't mess with node if search is currently matching
    #node.style("stroke", (n) -> if !n.searched then strokeFor(n) else "#555")
    #  .style("stroke-width", (n) -> if !n.searched then 1.0 else 2.0)
    if link
      link.attr("stroke-opacity", 0.8)
        
  iconFor = (i) ->
    icons[i]
  
  strokeFor = (d) ->
    d3.rgb(nodeColors(d.item_class)).darker().toString()

  
    
  # Adjusts x/y for each node to
  # push them towards appropriate location.
  # Uses alpha to dampen effect over time.
  moveToRadialLayout = (alpha) ->
    k = alpha * 0.1
    (d) ->
      centerNode = groupCenters(d.artist)
      d.x += (centerNode.x - d.x) * k
      d.y += (centerNode.y - d.y) * k
      
  return network



    
    
$ ->
  myNetwork = Network()
  
  myNetwork("#vis", connections)
  
  d3.selectAll("#mark a").on "click", (d) ->
    mark = d3.select(this).attr("id")
    myNetwork.markNodes(mark)
