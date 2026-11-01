"""Optional official schema checks, pinned and offline; no query engine."""
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/'examples/schemas'
registry=Registry()
for filename,alias in [('core.json','core-spec/ossie-schema.json'),('ontology.json','ontology/ontology.json'),('mapping.json','ontology/mapping.json')]:
    document=json.loads((SCHEMAS/filename).read_text())
    resource=Resource.from_contents(document)
    for uri in (document['$id'],'https://raw.githubusercontent.com/apache/ossie/main/'+alias):
        registry=registry.with_resource(uri,resource)
errors=[]
provenance=json.loads((SCHEMAS/'provenance.json').read_text())
for file,digest in provenance['files'].items():
    if hashlib.sha256((SCHEMAS/file).read_bytes()).hexdigest()!=digest: errors.append(file+': hash mismatch')
for kind,schema_file in [('semantic','core.json'),('ontology','ontology.json'),('mapping','mapping.json')]:
    document=json.loads((ROOT/f'examples/commerce.{kind}.json').read_text())
    schema=json.loads((SCHEMAS/schema_file).read_text())
    Draft202012Validator.check_schema(schema)
    for error in Draft202012Validator(schema,registry=registry).iter_errors(document):
        errors.append(f'{kind}: {list(error.path)} {error.message}')
mapping=json.loads((ROOT/'examples/commerce.mapping.json').read_text())
for ref,kind in [('ontology_ref','ontology'),('semantic_model_ref','semantic')]:
    document=json.loads((ROOT/'examples'/mapping[ref]['iri']).read_text())
    if document['name']!=mapping[ref]['name']:errors.append(ref+': identity mismatch')
report={'status':'fail' if errors else 'pass','commit':provenance['commit'],'schemas':3,'errors':errors,'limitations':'schema shape and document names only; not a general cross-reference, expression or semantic equivalence validator'}
(ROOT/'reports/ossie-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
