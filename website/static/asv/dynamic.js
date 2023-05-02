export class DynamicFilter {
  formInputs = {
    originalInputs: {},
    currentInputs: {},
  };
  constructor(inputs) {
    this.formInputs.originalInputs = inputs;
  }

  parseForm() {
    const form = document.getElementById("filter-trucks-form");

    const values = Object.fromEntries(new FormData(form));

    for (let i = 0; i < Object.keys(values).length; i++) {
        const select = document.getElementById(`${values[i]}`);
        const options = select.options.map((option) => option.innerHTML);
        this.formInputs.originalInputs[values[i]] = options;
    };
  }

  resetFilters() {
    for (const [key, value] of Object.entries(this.formInputs.originalInputs)) {
        this.formInputs.currentInputs[key] = value;
        const options = this.createOptionsFactory(value);
        const el = document.getElementById(`${key}`);
  
        if (el) el.replaceChildren(...options);
      }
  }

  changeFilters(data) {
    let values = {};

    const keys = Object.keys(data[0]);
    for (let i = 0; i < data.length; i++) {
        for (n = 0; n < keys.length; n++) {
            const vals = values[keys[n]] || []
            values[keys[n]] = [...vals, data[i][keys[n]]];
        }
    }

    for (const [key, value] of Object.entries(values)) {
        this.formInputs.currentInputs[key] = value;
        const options = this.createOptionsFactory(value);
        const el = document.getElementById(`${key}`);
  
        if (el) el.replaceChildren(...options);
      }
  }

  static createOptionsFactory(inputs) {
    let elements = [];
    for (let i = 0; i < inputs.length; i++) {
        const el = document.createElement('option');
        el.value = inputs[i];
        el.innerHTML = inputs[i];
        elements.push(el);
    }
    return elements;
  }
}