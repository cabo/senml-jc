#!/usr/bin/env ruby

# ruby senml2cbor.rb senml-data.json > senml-data.cbor
# (reads from stdin if no argument given)
#
# Installation: do `gem install cbor` first

require 'json'
require 'cbor'
require 'base64'

MAPPINGS = Hash.new {|h, k| k}

DATA.read.scan(/([-\w]+)\s*=\s*([-\w]+)/) do |n, v|
  begin
    MAPPINGS[n] = Integer(v)
  rescue ArgumentError
  end
end

# p MAPPINGS

class Array
  def cborify_senml
    map(&:cborify_senml)
  end
end

class Hash
  def cborify_senml
    Hash[map { |k, v|
           k = MAPPINGS[k]
           if k == 8 # vd (value, data)
             v = Base64.urlsafe_decode64(v)
           else
             v = v.cborify_senml
           end
           [k, v]
    }]
  end
end

if ENV["FLOAT"] == "half"

# This hacks off precision to 10 bits of mantissa so CBOR can generate
# half floats.
class Float
  def cborify_senml
    short = [[self].pack("g").unpack("N")[0] & 0xFFFFE000].pack("N").unpack("g")[0]
    # warn [short, short.to_cbor.size].inspect
    if short.to_cbor.size == 3
      short
    else
      self
    end
  end
end

elsif ENV["FLOAT"] == "single"

# This converts floating point precision so CBOR can generate
# single floats.
class Float
  def cborify_senml
    short = [[self].pack("g").unpack("N")[0]].pack("N").unpack("g")[0]
    # warn [short, short.to_cbor.size].inspect
    if short.to_cbor.size == 5
      short
    else
      self
    end
  end
end

end

class Object
  def cborify_senml
    self
  end
end

data = JSON.load(ARGF)
# p data.cborify_senml
print data.cborify_senml.to_cbor

# Below, a copy of senml-cbor.cddl so this is a freestanding program;
# need to remember to update this copy whenever we update
# senml-cbor.cddl
__END__

bver = -1  n  = 0   s  = 5
bn  = -2   u  = 1   t  = 6
bt  = -3   v  = 2   ut = 7
bu  = -4   vs = 3   vd = 8
bv  = -5   vb = 4
bs  = -6

binary-value = bstr
