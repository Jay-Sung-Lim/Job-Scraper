def save_to_file(platform, file_name, jobs):
  file = open(f"{platform}_{file_name}.csv", "w")
  file.write("Position,Compnay,Location,URL\n")

  for job in jobs:
    file.write(
      f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n")

  file.close()