---
title: Scaling to exabytes and beyond
source: https://dropbox.tech/infrastructure/magic-pocket-infrastructure
author: Akhil Gupta
published: '2016-03-14'
site: dropbox.tech
clipped: '2026-09-20'
---

# Scaling to exabytes and beyond

Years ago, we called Dropbox a [“Magic Pocket”](https://www.youtube.com/watch?v=QULM7M98TLo) because it was designed to keep all your files in one convenient place. Dropbox has evolved from that simple beginning to become one of the most powerful and ubiquitous collaboration platforms in the world. And when our scale required building our own dedicated storage infrastructure, we named the project “Magic Pocket.” Two and a half years later, we’re excited to announce that we’re now storing and serving over 90% of our users’ data on our custom-built infrastructure.

Dropbox was founded by engineers, and the ethos of technical innovation is fundamental to our culture. For our users, this means that we’ve created a product that just works. But there’s a lot that happens behind the scenes to create that simple user experience.

We’ve grown enormously since launching in 2008, surpassing 500 million signups and 500 petabytes (i.e., 5 followed by 17 zeroes!) of user data. That’s almost 14,000 times the text of all the books in the Library of Congress. To give you a sense of the incredible growth we’ve experienced, we had only about 40 petabytes of user data when I joined in 2012. In the 4 years since, we’ve seen over 12x growth.

Dropbox stores two kinds of data: file content and metadata about files and users. We’ve always had a hybrid cloud architecture, hosting metadata and our web servers in data centers we manage, and storing file content on Amazon. We were an early adopter of Amazon S3, which provided us with the ability to scale our operations rapidly and reliably. Amazon Web Services has, and continues to be, an invaluable partner—we couldn’t have grown as fast as we did without a service like AWS.

As the needs of our users and customers kept growing, we decided to invest seriously in building our own in-house storage system. There were a couple reasons behind this decision. First, one of our key product differentiators is performance. Bringing storage in-house allows us to customize the entire stack end-to-end and improve performance for our particular use case. Second, as one of the world’s leading providers of cloud services, our use case for block storage is unique. We can leverage our scale and particular use case to customize both the hardware and software, resulting in better unit economics.

We knew we’d be building one of only a handful of exabyte-scale storage systems in the world. It was clear to us from the beginning that we’d have to build everything from scratch, since there’s nothing in the open source community that’s proven to work reliably at our scale. Few companies in the world have the same requirements for scale of storage as we do. And even fewer have higher standards for safety and security. We built reliability and security into our design from the start, ensuring that the system stores the data in a safe and secure manner, and is highly available. The data is encrypted at rest, and the system is designed to provide annual data durability of over 99.9999999999%, and availability of over 99.99%.

## How did we make this happen?

Code development: Magic Pocket became a major initiative in the summer of 2013. We’d built a small prototype as a proof of concept prior to this to get a sense of our workloads and file distributions. Software was a big part of the project, and we iterated on how to build this in production while validating rigorously at every stage. The innovation focused on creating a clean design that would scale from zero to one of the largest storage systems in the world, and automation that would allow our small team to maintain an enormous amount of hardware. We needed to test and audit the reliability of the system for the highest levels of data durability and availability.

**Dark launch:** In August 2014, we embarked on our "dark launch," at which point we were mirroring data between two regional locations and considered the system ready to store user data. Of course, being Dropbox, we kept extra backups for another 6 months after this date just in case.

**Launch day:** February 27, 2015 was D-day. For the first time in the history of Dropbox, we began storing and serving user files exclusively in-house. Once we validated our new infrastructure, we set an aggressive goal of scaling the system to more than 500PB in six months.

**BASE Jump:** On April 30, 2015, we began the race to install additional servers in three regional locations fast enough to keep up with the flow of data. To make this all work, we built a high-performance network from our servers which allowed us to transfer data at a peak rate of over half a terabit per second. Because our schedule left so little time to “open the parachute,” we called this part of the project BASE Jump. On the hardware side, we were pushing up against the limitations of how many racks of hardware could fit in the loading dock at one time.

**Successful landing:** Our goal was to serve 90% of our data from in-house infrastructure by October 30, 2015. We actually hit the mark almost a month early, on October 7, 2015. The team not only delivered on time, but also achieved this significant technical undertaking without any major service disruptions or any loss of data.

This is an exciting milestone and the start of more innovation to come. We’ll continue to invest in our own infrastructure as well as partner with Amazon where it makes sense for our users, particularly globally. Later this year, we’ll expand our relationship with AWS [to store data in Germany for European business customers](https://blogs.dropbox.com/business/2016/02/dropbox-is-growing-in-europe/) that request it. Protecting and preserving the data our users entrust us with is our top priority at all times.

This is Dropbox engineering—always aiming higher!

This is the first of a series of blog posts about the Magic Pocket. Over the next month we’ll share a lot of the technical details around what we learned from building our own high-performance cloud infrastructure. Stay tuned.
