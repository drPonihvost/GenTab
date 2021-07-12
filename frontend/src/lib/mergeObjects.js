export const mergeObjects = (objects) => {
  // Не знаю как должно работать :(

  const resultMarkers = {};
  const resultObject = {
    id: '',
    name: ''
  };

  Object.entries(objects).forEach(([objectName, object], index) => {
    const { id, markers } = object;

    const idPart = index ? ` + ${id}` : id;
    resultObject.id = resultObject.id + idPart;

    const namePart = index ? ` + ${objectName}` : objectName;
    resultObject.name = resultObject.name + namePart;

    markers.forEach((marker) => {
      const resultMarker = resultMarkers[marker.name];

      if (resultMarker) {
        const result = { ...resultMarker };

        for (const [key, value] of Object.entries(marker)) {
          if (result[key]) {
            result[key] = result[key] + ` + ${value}`;
          } else {
            result[key] = value;
          }
        }

        resultMarkers[marker.name] = result;
      } else {
        resultMarkers[marker.name] = marker;
      }
    });
  });

  return {
    ...resultObject,
    markers: Object.values(resultMarkers)
  };
};
