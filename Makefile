JSON_SOURCES = $(wildcard json/*.json)
FILENAMES = $(JSON_SOURCES:json/%=%)
CBOR_HALF_RESULTS = $(FILENAMES:%.json=cbor-half/%.cbor)
CBOR_RESULTS = $(FILENAMES:%.json=cbor/%.cbor)

all: table.md lora-rx-leaf.md

table.md: results
	ruby mktable.rb > $@.new
	mv $@.new $@
	cat $@

lora-rx-leaf.md: table.md
	cat $< | python3 energy.py > $@

results: $(CBOR_RESULTS) $(CBOR_HALF_RESULTS)

cbor/%.cbor: json/%.json
	ruby senml-json2cbor.rb $< > $@.new
	mv $@.new $@

cbor-half/%.cbor: json/%.json
	env FLOAT=half ruby senml-json2cbor.rb $< > $@.new
	mv $@.new $@


