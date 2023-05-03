export class DynamicFilter {
  formInputs = {
    originalInputs: {},
    currentInputs: {},
  };
  form = null;
  constructor() {
    const form = document.getElementById("filter-trucks-form");
    this.form = form;

    const values = Object.fromEntries(new FormData(form));
    const keys = Object.keys(values);

    for (let i = 0; i < keys.length; i++) {
      const select = document.getElementById(`${keys[i]}`);
      const children = Object.values(select.options);
      const options = children.map((option) => option.innerHTML);
      this.formInputs.originalInputs[keys[i]] = options;
    }
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
      for (let n = 0; n < keys.length; n++) {
        const vals = values[keys[n]] || [];
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

  createOptionsFactory(inputs) {
    let elements = [];
    for (let i = 0; i < inputs.length; i++) {
      const el = document.createElement("option");
      el.value = inputs[i];
      el.innerHTML = inputs[i];
      elements.push(el);
    }
    return elements;
  }
}

export async function onChangeSelect(e) {
  let values = {};
  const entry = Object.fromEntries(new FormData(this));
  for (const [key, value] of Object.entries(entry)) {
    if (value.length > 0) values[key] = value;
  }
  const params = new URLSearchParams(values);

  try {
    const response = await fetch("/trucks?" + params.toString(), {
      headers: {
        "Content-Type": "application/json",
      },
      method: "GET",
      credentials: "include",
    });
    const { data } = await response.json();
    this.filter.changeFilters(data);
  } catch (err) {
    console.error(err);
  }
}
