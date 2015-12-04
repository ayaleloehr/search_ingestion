#tutorial: http://jasonseifer.com/2010/04/06/rake-tutorial
task :index_website, [:arg1,:arg2] do |t,args|
  sh "python generate_index.py #{args[:arg1]} #{args[:arg2]}"
end

