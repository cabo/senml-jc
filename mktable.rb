require 'json'

files = Dir["json/*.json"].map{ |x| x.gsub("json/", "").gsub(".json", "")}

def sz(fn)
  File.stat(fn).size
end

puts "| %20s | json | cbor | half | red." % "example"
files.each do |f|
  puts "| %20s | %4d | %4d | %4d | %d %%" % [f,
       j = JSON.generate(JSON.parse(File.read("json/#{f}.json"))).size,
       c = sz("cbor/#{f}.cbor"),
       sz("cbor-half/#{f}.cbor"),
       ((1 - c.to_f/j.to_f) * 100).round(2)
]
end
