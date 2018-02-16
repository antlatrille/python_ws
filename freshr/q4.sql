CREATE DATABASE freshr;

CREATE SCHEMA ads;

CREATE EXTENSION "uuid-ossp";

CREATE TABLE public."user"
(
  id          UUID DEFAULT uuid_generate_v4() PRIMARY KEY                NOT NULL,
  facebook_id UUID                                                       NOT NULL,
  preferences JSONB,
  profile     JSONB,
  created     TIMESTAMP WITH TIME ZONE DEFAULT now()                     NOT NULL
);
CREATE UNIQUE INDEX user_id_uindex
  ON public."user" (id);
CREATE UNIQUE INDEX user_facebook_id_uindex
  ON public."user" (facebook_id);


CREATE TABLE public.article
(
  id        UUID DEFAULT uuid_generate_v4() PRIMARY KEY                NOT NULL,
  url       VARCHAR                                                    NOT NULL,
  short_url VARCHAR,
  summary   TEXT,
  metadata  JSONB,
  created   TIMESTAMP WITH TIME ZONE DEFAULT now()                     NOT NULL,
  updated   TIMESTAMP WITH TIME ZONE DEFAULT now()                     NOT NULL
);
CREATE UNIQUE INDEX article_id_uindex
  ON public.article (id);
CREATE UNIQUE INDEX article_url_uindex
  ON public.article (url);


-- The command list, or the destination set of what can output the NLP module
CREATE TABLE public.command
(
  id      UUID DEFAULT uuid_generate_v4()                NOT NULL,
  name    VARCHAR PRIMARY KEY                            NOT NULL,
  created TIMESTAMP WITH TIME ZONE DEFAULT now()         NOT NULL
);
CREATE UNIQUE INDEX command_id_uindex
  ON public.command (id);
CREATE UNIQUE INDEX command_name_uindex
  ON public.command (name);

CREATE TABLE public.user_message
(
  id         UUID DEFAULT uuid_generate_v4() PRIMARY KEY                NOT NULL,
  user_id    UUID                                                       NOT NULL,
  command_id UUID                                                       NOT NULL,
  content    VARCHAR                                                    NOT NULL,
  created    TIMESTAMP WITH TIME ZONE DEFAULT now()                     NOT NULL,
  CONSTRAINT user_message_user_id_fk FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
  CONSTRAINT user_message_command_id_fk FOREIGN KEY (command_id) REFERENCES command (id)
);
CREATE UNIQUE INDEX user_message_id_uindex
  ON public.user_message (id);

CREATE TABLE public.sent_message
(
  id       UUID DEFAULT uuid_generate_v4() PRIMARY KEY                NOT NULL,
  user_id  UUID                                                       NOT NULL,
  type     VARCHAR                                                    NOT NULL, -- is it a push, an ad, an answer?
  content  TEXT                                                       NOT NULL,
  metadata JSONB,
  created  TIMESTAMP WITH TIME ZONE DEFAULT now()                     NOT NULL,
  read     TIMESTAMP WITH TIME ZONE,
  CONSTRAINT sent_message_user_id_fk FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX sent_message_id_uindex
  ON public.sent_message (id);


CREATE TABLE analysis.model_history
(
  sha256   TEXT                                   NOT NULL -- signature of the prediction model
    CONSTRAINT model_history_pkey
    PRIMARY KEY,
  created  TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  metadata JSONB
);

CREATE TABLE analysis.article_parameters
(
    article_id UUID NOT NULL,
    model_sha256 TEXT NOT NULL,
    values JSONB NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (article_id, model_sha256)
)
;

