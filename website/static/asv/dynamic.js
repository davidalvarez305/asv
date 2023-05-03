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
      const options = this.createOptionsFactory(["", ...new Set(value)]);
      const htmlKey = HTML_DICTIONARY[key];
      const el = document.getElementById(`${htmlKey}`);
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

const HTML_DICTIONARY = {
  year: "vehicle_details__year",
  make: "vehicle_details__make_id",
  model: "vehicle_details__model_id",
  trim: "vehicle_details__trim_id",
  cabtype: "vehicle_details__cabtype",
  fueltype: "vehicle_details__fueltype",
  enginesize: "vehicle_details__enginesize",
  odometerreadingdescription: "vehicle_details__odometerreadingtypedescription",
  drivelinetype: "vehicle_details__drivelinetype",
  starts_at_checkin: "vehicle_details__vehicle_condition__starts_at_checkin",
  runs_and_drives: "vehicle_details__vehicle_condition__runs_and_drives",
  air_bags_deployed: "vehicle_details__vehicle_condition__air_bags_deployed",
  damage_description_primary: "vehicle_details__vehicle_condition__damage_description_primary",
  loss_type: "vehicle_details__vehicle_condition__loss_type",
};
