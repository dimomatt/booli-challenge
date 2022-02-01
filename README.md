This is a simple functional(ish) implementation of a program that will return a list of ECS formatted json objects contianing data regarding CVE's from the last "d" days. It was built to have minimal requirements, and a dockerfile that hopefully works is included. 

I tried to design this in a way that would allow for simple extensibility in the event that new data shows up, or I discover that I am "missing" a field that should be mapped. Adding a new getter for data would require adding the map function that adds it in lib/map.py, and adding it to the list of extractors in map.py Adding output modes (if you want to hook in to a different database) would also require adding just one more function in the "outputs" section, adding an argument to the parser, and adding that output to the main function.

Some deficiences here are:
  - I have not done a great job of mapping data to ecs fields, I would need to spend more time in the docs to do that well.
  - The extractors are more brittle to data being missing than I would like. I think a future implementation would either autogenerate getters from a csv file that maps NVD fields to ECS fields, which would allow me to do more error checking at a field by field level, but I feel okay about this solution. 
  - Testing! I felt that most of these functions are pretty easy to understand, but testing is always better than no testing. I will probably add some tests tomorrow.
